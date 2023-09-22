from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # fields='__all__'
        fields = ("id", "name", "email", "password", "role","phonenumber")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data["name"],
            email=validated_data["email"],
            role=validated_data["role"],
            phonenumber=validated_data["phonenumber"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
    
class UserloginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            raise serializers.ValidationError('Cannot find the given email address')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid Credentials')

        return super().validate(attrs)