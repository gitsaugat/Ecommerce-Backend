
from django.urls import path
from .api_provider import StripeProvider
urlpatterns = [
    path('payment/', StripeProvider.as_view(), name="stripe_provider")
]
