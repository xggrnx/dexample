from rest_framework import serializers

from market.models import Price, Country, Product


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'product', 'quantity', 'cost']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'language_locale', 'currency_code']


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для отображения и создания товара в корзине
    """
    class Meta:
        model = Product
        fields = [
            'id',
            'ext_id',
        ]
