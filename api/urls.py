from django.urls import path
from api.views import *
from .import views
from rest_framework_simplejwt.views import (TokenRefreshView)

urlpatterns = [
    path("",views.home),
    path("login/", LoginApiView.as_view(), name="login"),
    path("signup/", SignupApiView.as_view(), name="signup"),
    path("api/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',views.logout_view)


    
    ]