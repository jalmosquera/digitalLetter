"""
Email service for sending order confirmations.
"""
import os
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.mime.image import MIMEImage
from smtplib import SMTPException
from socket import timeout as SocketTimeout

logger = logging.getLogger(__name__)


def send_order_confirmation_emails(order_data, user_email, company_email):
    """
    Send order confirmation emails to both customer and company.

    Args:
        order_data (dict): Order information including items, delivery info, totals
        user_email (str): Customer email address
        company_email (str): Company email address

    Returns:
        dict: Status of email sending {customer: bool, company: bool}
    """
    results = {'customer': False, 'company': False}

    # Prepare data for templates
    language = order_data.get('language', 'es')

    # Send customer email
    try:
        customer_email_sent = _send_customer_email(order_data, user_email, language)
        results['customer'] = customer_email_sent
        logger.info(f"Customer email sent successfully to {user_email}")
    except (SMTPException, SocketTimeout, OSError) as e:
        logger.error(f"Error sending customer email to {user_email}: {type(e).__name__} - {e}")
        results['customer'] = False
    except Exception as e:
        logger.exception(f"Unexpected error sending customer email: {e}")
        results['customer'] = False

    # Send company email
    try:
        company_email_sent = _send_company_email(order_data, company_email)
        results['company'] = company_email_sent
        logger.info(f"Company email sent successfully to {company_email}")
    except (SMTPException, SocketTimeout, OSError) as e:
        logger.error(f"Error sending company email to {company_email}: {type(e).__name__} - {e}")
        results['company'] = False
    except Exception as e:
        logger.exception(f"Unexpected error sending company email: {e}")
        results['company'] = False

    return results


def _send_customer_email(order_data, recipient_email, language='es'):
    """Send order confirmation email to customer."""

    # Email subject
    if language == 'es':
        subject = f"✓ Pedido Confirmado #{order_data['order_id']} - Equus Pub"
    else:
        subject = f"✓ Order Confirmed #{order_data['order_id']} - Equus Pub"

    # Render HTML template
    html_content = render_to_string(
        'emails/customer_order_confirmation.html',
        {
            'language': language,
            'order_id': order_data['order_id'],
            'user_name': order_data['user_name'],
            'delivery_street': order_data['delivery_info']['street'],
            'delivery_house_number': order_data['delivery_info']['house_number'],
            'delivery_location': order_data['delivery_info']['location'],
            'phone': order_data['delivery_info']['phone'],
            'notes': order_data['delivery_info'].get('notes', ''),
            'items': order_data['items'],
            'total_price': order_data['total_price'],
        }
    )

    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body='',  # Plain text version (empty for now)
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email]
    )

    email.attach_alternative(html_content, "text/html")

    # Attach logo as inline image
    logo_path = os.path.join(settings.BASE_DIR, 'apps/orders/static/images/logoEquss.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_img = MIMEImage(f.read())
            logo_img.add_header('Content-ID', '<logo>')
            logo_img.add_header('Content-Disposition', 'inline', filename='logoEquss.png')
            email.attach(logo_img)

    # Send email
    email.send()
    return True


def _send_company_email(order_data, recipient_email):
    """Send order notification email to company."""

    subject = f"🔔 Nuevo Pedido #{order_data['order_id']} - {order_data['user_name']}"

    # Render HTML template
    html_content = render_to_string(
        'emails/company_order_notification.html',
        {
            'order_id': order_data['order_id'],
            'user_name': order_data['user_name'],
            'user_email': order_data.get('user_email', ''),
            'delivery_street': order_data['delivery_info']['street'],
            'delivery_house_number': order_data['delivery_info']['house_number'],
            'delivery_location': order_data['delivery_info']['location'],
            'phone': order_data['delivery_info']['phone'],
            'notes': order_data['delivery_info'].get('notes', ''),
            'items': order_data['items'],
            'total_price': order_data['total_price'],
        }
    )

    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body='',  # Plain text version
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email]
    )

    email.attach_alternative(html_content, "text/html")

    # Send email
    email.send()
    return True
