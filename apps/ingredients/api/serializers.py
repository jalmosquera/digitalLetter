from rest_framework import serializers
from apps.ingredients.models import Ingredient
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


class IngredientSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Ingredient)

    class Meta:
        model = Ingredient
        fields = ['id', 'translations', 'icon']
        

    def create(self, validated_data):
        translations = validated_data.pop('translations', {})
        instance = Ingredient.objects.create(**validated_data)
        for lang_code, fields in translations.items():
            instance.set_current_language(lang_code)
            for attr, value in fields.items():
                setattr(instance, attr, value)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        translations = validated_data.pop('translations', {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        for lang_code, fields in translations.items():
            instance.set_current_language(lang_code)
            for attr, value in fields.items():
                setattr(instance, attr, value)
        instance.save()
        return instance
