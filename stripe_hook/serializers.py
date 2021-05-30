from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import StripePayment, StripeOrderInfo
from store.models import Order
from store.serializers import OrderSerializer  # type:ignore
from users.serializers import UserSerializer  # type:ignore


class PaymentsSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=False)

    class Meta:
        model = StripePayment
        fields = '__all__'
        read_only_fields = ['id', 'order']

    def create(self, validated_data):
        print("hello")
        order_instance = Order.objects.get(id=validated_data.pop('order'))
        instance = StripePayment.objects.create(
            order=order_instance, **validated_data)
        return instance


class OrderInfoSerializer(serializers.ModelSerializer):
    stripe_payment_object = PaymentsSerializer()

    class Meta:
        model = StripeOrderInfo
        fields = [
            'id',
            'stripe_paymen_object',
            'full_name',
            'phone_number',
            'email',
            'delivery_address'
        ]
