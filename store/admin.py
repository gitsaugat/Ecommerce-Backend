from django.contrib import admin
from .models import Category, Products, Order, OrderItem
# Register your models here.

admin.site.site_header = "Ecommerce"
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(OrderItem)
