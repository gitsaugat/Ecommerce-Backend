from django.db import models
from django.db.models.fields import related
from store.models import Order  # type:ignore
from django.contrib.auth.models import User
# Create your models here.

PAYMENT_CHOICES = [
    ['STRIPE', 'STRIPE']
]


class StripePayment(models.Model):
    order = models.ForeignKey(
        Order,  related_name='payments_order', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    payment_method = models.CharField(
        choices=PAYMENT_CHOICES, default='ESEWA', max_length=10, null=False, blank=False)
    card_number = models.CharField(
        max_length=200, null=False, blank=False)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.id)


class StripeOrderInfo(models.Model):
    payment_object = models.OneToOneField(
        StripePayment, related_name='stripe_payment_object', on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(
        max_length=200, default='John Doe', null=False, blank=False)
    phone_number = models.IntegerField(default=0, null=False, blank=False)
    email = models.EmailField(
        default="test@gmail.com", null=False, blank=False)
    delivery_address = models.CharField(
        max_length=200, default='Street Address', null=False, blank=False)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
