from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(
        source='product.name',
        read_only=True
    )
    price=serializers.CharField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    class Meta:
        model=Cart
        fields=[
            'id',
            'product',
            'product_name',
            'price',
            'quantity'
        ]