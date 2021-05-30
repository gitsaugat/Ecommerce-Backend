from django.contrib import admin
from .models import EsewaPayment, EsewaOrderInfo
# Register your models here.
admin.site.register(EsewaPayment)
admin.site.register(EsewaOrderInfo)
