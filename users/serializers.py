from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            "email",
            'username',
            'password',
            'password2',
        ]
        extra_kwargs = {
            "first_name": {'required': True},
            "last_name": {'required': True},
            "email": {'required': True},

        }

    def validate(self, attrs):
        for user in User.objects.all():
            if user.email == attrs['email']:
                raise serializers.ValidationError(
                    {'email': 'user with that email already exists'})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Both passwords should be same'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            email=validated_data["email"],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
