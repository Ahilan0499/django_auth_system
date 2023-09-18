from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.exceptions import AuthenticationFailed
# Create your views here.

class SignupApiView(APIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()

            status_code = status.HTTP_201_CREATED

            response = {
                "success": True,
                "statusCode": status_code,
                "message": "User successfully registered",
                "user": serializer.data,
            }

            return Response(response, status=status_code)


class LoginApiView(APIView):
     def post(self , request):
        email=request.data['email']
        password=request.data['password']

        user=User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("user not found")
        
        if not user.check_password(password):
            raise AuthenticationFailed("incorrect password")
        
        return Response(
            {
                'message':'success'
            }
        )