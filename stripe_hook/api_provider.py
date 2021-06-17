import secrets
from store.serializers import OrderSerializer  # type:ignore
import uuid
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from store.models import Order  # type:ignore
from .models import StripePayment, StripeOrderInfo
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_API_KEYS['sk']


class StripeProvider(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication,
                              TokenAuthentication, SessionAuthentication]

    def post(self, request, format=None):
        order, created = Order.objects.get_or_create(
            user=request.user, completed=not True)
        data = (request.data)
        token = request.data['token']['token']['id']
        user_data = request.data['user_data']

        if data:
            if order:
                get_total = order.get_cart_total()
                try:
                    charge = stripe.Charge.create(
                        amount=get_total,
                        currency='usd',
                        description='Charge for shopping',
                        source=token

                    )
                    order.completed = not order.completed
                    order.transaction_id = secrets.token_hex(28)
                    order.save()

                    payment = StripePayment.objects.create(
                        order=order,
                        amount=get_total,
                        payment_method='STRIPE',
                    )
                    payment.save()

                    order_info = StripeOrderInfo.objects.create(
                        payment_object=payment,
                        full_name=user_data['name'],
                        email=user_data['email'],
                        delivery_address=user_data['address'],
                        phone_number=user_data['contact_no']
                    )
                    order_info.save()
                except:
                    return Response('Couldnt Create Charge', status=401)
                return Response('Charge Created', status=200)
