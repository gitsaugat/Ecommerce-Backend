from rest_framework import serializers
from .models import Products,  Category, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = [
            'id',
            'name',
            'get_absolute_url',
            'description',
            'price',
            'get_image_url',
            'get_thumbnail_url',
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = [
            'quantity',
            'product'
        ]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    orderitem_orders = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'slug',
            'transaction_id',
            'completed',
            'orderitem_orders',
            'get_cart_total'
        ]




class CategorySearializer(serializers.ModelSerializer):

    category_products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'get_absolute_url',
            'category_products'
        ]
        read_only_fields = ['products']
