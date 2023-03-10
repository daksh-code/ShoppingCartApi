from unicodedata import name
from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    image = serializers.CharField()
    name = serializers.CharField()
    unit_price = serializers.FloatField()
    quantity = serializers.IntegerField()

class AddToCartSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    quantity = serializers.IntegerField()

class CartUpdateSerializer(serializers.Serializer):
    productId = serializers.CharField()
    quantity = serializers.IntegerField()

class ApplyCouponSerializer(serializers.Serializer):
    coupon_code = serializers.CharField()

class AddCouponSerializer(serializers.Serializer):
    name = serializers.CharField()
    min_order_value = serializers.FloatField()
    discount_percent = serializers.IntegerField()