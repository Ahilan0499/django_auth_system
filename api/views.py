from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .authentication import *
from django.contrib.auth import logout

# Create your views here.

import requests
from django.http import JsonResponse

def google_oauth_callback(request):
    if request.method == 'POST':
        # Assuming you have received the authorization code in the request data
        authorization_code = request.POST.get('code')  # Replace with your method of extracting the code

        # Define the token endpoint URL
        token_url = 'https://accounts.google.com/o/oauth2/token'

        # Prepare the data to send in the POST request
        data = {
            'code': '0d465111068746ad84',
            'client_id': '505313360289-8aucppmh24si91a9v4l2outojte9m5fi.apps.googleusercontent.com',
            'client_secret': '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',
            'redirect_uri': 'http://localhost:8000/accounts/google/login/callback/',
            'grant_type': 'authorization_code'
        }

        try:
            # Make the POST request to Google's token endpoint
            response = requests.post(token_url, data=data)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the JSON response
            token_data = response.json()

            # Extract the access token and refresh token
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')

            # Handle the tokens as needed, e.g., store them in the session or database

            # Return a JSON response indicating success
            return JsonResponse({'message': 'Authentication successful', 'access_token': access_token})

        except requests.exceptions.RequestException as e:
            # Handle network errors or other exceptions here
            return JsonResponse({'message': f"Error: {e}"}, status=400)
        except ValueError as ve:
            # Handle JSON parsing errors here
            return JsonResponse({'message': f"JSON Parsing Error: {ve}"}, status=400)

    # Handle other HTTP methods or render a response for GET requests
    return JsonResponse({'message': 'Invalid HTTP method'}, status=405)


def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")


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
     serializer_class = UserloginSerializer
     permission_classes = [AllowAny]
     def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = User.objects.get(email=email)
        
            access_token=create_access_token(user.id)
            refresh_token=create_refresh_taken(user.id)  
            return Response(
            {
              
            'accesss':access_token,
            'refresh':refresh_token

            })  
                 
        else:
            return Response(serializer.errors)
        