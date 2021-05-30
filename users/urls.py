from django.contrib.auth.models import User
from django.urls import path
from .views import UserListView, UserRegistrationView,  UserPasswordResetView
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('users/', UserListView.as_view(), name="user_list"),
    path('register/user/', UserRegistrationView.as_view(),
         name="user_registration"),
    path('user/token/', obtain_auth_token, name="obtain_token"),
    path('user/password/reset/',
         UserPasswordResetView.as_view(), name="password_reset")
]
