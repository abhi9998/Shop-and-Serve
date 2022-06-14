from rest_framework import serializers
from .models import Order, OrderGroup, OrderProduct


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = "__all__"

class OrderGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGroup
        fields = "__all__"