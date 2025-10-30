"""Orders API views module.

This module provides REST API viewsets for managing customer orders in the digital
menu system. Orders can be created by authenticated users, and viewed/managed
based on user permissions.

Typical usage example:
    GET /api/orders/ - List user's own orders (or all for staff)
    POST /api/orders/ - Create a new order (authenticated users only)
    GET /api/orders/{id}/ - Retrieve order details
    PATCH /api/orders/{id}/ - Update order status (staff only)
"""

from typing import Any

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from apps.orders.models import Order
from apps.orders.api.serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer
)


@extend_schema_view(
    list=extend_schema(
        tags=['orders'],
        description="List all orders. Regular users see only their orders, staff see all.",
        responses={
            200: OrderListSerializer(many=True),
        },
    ),
    create=extend_schema(
        tags=['orders'],
        description="Create a new order with delivery details and items.",
        request=OrderCreateSerializer,
        responses={
            201: OrderDetailSerializer,
            400: OpenApiResponse(description='Invalid data or unavailable products'),
        },
    ),
    retrieve=extend_schema(
        tags=['orders'],
        description="Retrieve order details.",
        responses={
            200: OrderDetailSerializer,
            403: OpenApiResponse(description='Not your order'),
            404: OpenApiResponse(description='Not found'),
        },
    ),
    partial_update=extend_schema(
        tags=['orders'],
        description="Update order status (staff only).",
        responses={
            200: OrderDetailSerializer,
            400: OpenApiResponse(description='Invalid data'),
            403: OpenApiResponse(description='Permission denied'),
        },
    ),
)
class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for managing customer orders.

    Provides CRUD operations for orders with user-based filtering.
    Regular users can only create and view their own orders.
    Staff users can view and update all orders.

    Permissions:
        - list: Authenticated users (filtered by user)
        - create: Authenticated users
        - retrieve: Order owner or staff
        - update/partial_update: Staff only
        - destroy: Not allowed

    Attributes:
        permission_classes: Requires authentication for all actions.
        http_method_names: Allowed HTTP methods (no DELETE).

    Example:
        >>> # Create order (from view)
        >>> POST /api/orders/
        >>> {
        ...     "delivery_address": "Calle 123",
        ...     "delivery_location": "Madrid",
        ...     "phone": "+34623736566",
        ...     "items": [
        ...         {"product": 5, "quantity": 2},
        ...         {"product": 7, "quantity": 1}
        ...     ]
        ... }
        >>> # Response: 201 Created with order details

    Note:
        - Users automatically set as order owner on creation
        - Orders cannot be deleted (only cancelled by updating status)
        - Staff can update order status to track fulfillment
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']  # No DELETE

    def get_queryset(self):
        """Get queryset filtered by user permissions.

        Regular users see only their own orders.
        Staff users see all orders.

        Returns:
            QuerySet: Filtered orders queryset.

        Example:
            >>> # Regular user sees only their orders
            >>> user.orders.all()
            >>> # Staff sees all orders
            >>> Order.objects.all()
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get_serializer_class(self) -> type[Serializer]:
        """Return appropriate serializer based on action.

        Returns:
            Serializer: OrderListSerializer for list,
                       OrderDetailSerializer for retrieve,
                       OrderCreateSerializer for create.

        Example:
            >>> viewset.action = 'list'
            >>> viewset.get_serializer_class()
            <class 'OrderListSerializer'>
        """
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderCreateSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new order.

        Creates order with authenticated user as owner and provided items.

        Args:
            request: HTTP request with order data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: 201 with created order details or 400 with errors.

        Example:
            >>> POST /api/orders/
            >>> {
            ...     "delivery_address": "Calle 123",
            ...     "delivery_location": "Madrid",
            ...     "phone": "+34623736566",
            ...     "items": [{"product": 5, "quantity": 2}]
            ... }
            >>> # Returns 201 with OrderDetailSerializer data
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)

        # Return detailed order response
        detail_serializer = OrderDetailSerializer(order)
        return Response(
            detail_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Update order (status only, staff only).

        Allows staff to update order status. Regular users cannot update.

        Args:
            request: HTTP request with update data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: 200 with updated order or 403 if not staff.

        Example:
            >>> PATCH /api/orders/1/
            >>> {"status": "confirmed"}
            >>> # Returns 200 with updated order
        """
        if not request.user.is_staff:
            return Response(
                {"detail": "Only staff can update orders."},
                status=status.HTTP_403_FORBIDDEN
            )

        instance = self.get_object()

        # Only allow status updates
        if 'status' in request.data:
            instance.status = request.data['status']
            instance.save()

        serializer = OrderDetailSerializer(instance)
        return Response(serializer.data)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieve order details.

        Users can only view their own orders, staff can view all.

        Args:
            request: HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: 200 with order details or 403 if not owner.

        Example:
            >>> GET /api/orders/1/
            >>> # Returns order details if user is owner or staff
        """
        instance = self.get_object()

        # Check permission: owner or staff
        if instance.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You can only view your own orders."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
