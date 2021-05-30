from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated,  AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
# Create your views here.


class UserListView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication,
                              BasicAuthentication, SessionAuthentication]

    def get(self, request, format=None):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("account created", status=200)
        else:
            return Response(serializer.errors, status=400)


class UserPasswordResetView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,
                              SessionAuthentication, BasicAuthentication]

    def post(self, request, format=None):
        pass
