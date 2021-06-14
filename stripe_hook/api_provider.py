import re
from store.serializers import OrderSerializer  # type:ignore
import uuid
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import PaymentsSerializer, OrderInfoSerializer
from store.models import Order  # type:ignore
from .models import StripePayment, StripeOrderInfo
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
import math


stripe_api_key = {
    'pk': 'pk_test_51ICy9QFynavadh4l6xAqRalcKAw5Cj3QZVKmTc11egr4X4jTaMmPZ5jemUZFnIxw5ri0hbLzhpawVZOBOsnCj0UH00geQMlFiH',
    'sk': 'sk_test_51ICy9QFynavadh4lw5ckTLdbJhMUExxI9Z141XSMle0p9pJgM3ZYElfVQspkT6WIOT7jgwACnvJScehKDldJP4M800v2em63Fh'
}

stripe.api_key = stripe_api_key['sk']


class StripeProvider(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication,
                              TokenAuthentication, SessionAuthentication]

    def post(self, request, format=None):
        order, creatd = Order.objects.get_or_create(
            user=request.user, completed=not True)
        request.data['card_number'] = "hello"
        request.data['amount'] = order.get_cart_total()
        request.data['order'] = order.id
        if order.get_cart_total() > 1:

            newpayment = PaymentsSerializer(data=request.data)
            new_order = OrderInfoSerializer(data=request.data)

            if newpayment.is_valid():
                newpayment.payments_order = order
                newpayment.save()
            else:
                return Response(newpayment.errors, status=400)

            if new_order.is_valid():
                new_order.stripe_payment_object = newpayment
                new_order.save()
            else:

                return Response(new_order.errors, status=400)

            order.completed = True
            order.transaction_id = uuid.uuid4()
            order.save()
            try:
                intent = stripe.PaymentIntent.create(
                    amount=order.get_cart_total(),
                    currency='usd'
                )
            except Exception as e:
                StripeOrderInfo.objects.get(payment_object=newpayment).delete()
                StripePayment.objects.get(id=newpayment.id).delete()
                return Response(str(e), status=400)
            try:
                payment = PaymentsSerializer(newpayment)
                order_ = OrderInfoSerializer(new_order)
                return Response({
                    'payment': payment,
                    'order': order,
                    'status': 'success'
                }, status=200)
            except Exception as e:
                return Response(str(e), status=400)
        else:
            return Response('Your transaction amount must be greater than 1', status=400)
