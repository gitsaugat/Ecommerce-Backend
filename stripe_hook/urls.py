
from django.urls import path
from .api_provider import StripeProvider
urlpatterns = [
    path('stripe/payment/', StripeProvider.as_view(), name="stripe_provider")
]
