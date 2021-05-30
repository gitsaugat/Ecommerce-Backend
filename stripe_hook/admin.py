from django.contrib import admin
from .models import StripePayment, StripeOrderInfo
# Register your models here.

admin.site.register(StripePayment)
admin.site.register(StripeOrderInfo)
