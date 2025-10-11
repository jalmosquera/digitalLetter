from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from apps.products.models import Products
from apps.categories.api.serializers import CategorySerializerGet
from apps.categories.models import Category
from apps.ingredients.api.serializers import IngredientSerializer
from apps.ingredients.models import Ingredients


class ProductSerializerPost(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Products)
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredients.objects.all(),
        required=False
    )

    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        translations = validated_data.pop('translations', {})
        categories = validated_data.pop('categories', [])
        ingredients = validated_data.pop('ingredients', [])
        instance = Products.objects.create(**validated_data)
        instance.categories.set(categories)
        instance.ingredients.set(ingredients)  # ✅ añadimos ingredientes
        for lang_code, translation_fields in translations.items():
            instance.set_current_language(lang_code)
            for attr, value in translation_fields.items():
                setattr(instance, attr, value)
            instance.save()
        return instance

    def update(self, instance, validated_data):
        translations = validated_data.pop('translations', {})
        categories = validated_data.pop('categories', None)
        ingredients = validated_data.pop('ingredients', None)
        if categories is not None:
            instance.categories.set(categories)
        if ingredients is not None:
            instance.ingredients.set(ingredients)  # ✅ actualizamos ingredientes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        for lang_code, translation_fields in translations.items():
            instance.set_current_language(lang_code)
            for attr, value in translation_fields.items():
                setattr(instance, attr, value)
        instance.save()
        return instance


class ProductSerializerGet(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Products)
    categories = CategorySerializerGet(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)  # ✅ incluimos ingredientes

    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = f"{data['price']} €"  # ✅ corregido para mostrar como string con €
        return data
