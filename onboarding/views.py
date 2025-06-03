from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdminLoginSerialisers,AdminForgotPasswordRequestSerializer, AdminForgotPasswordOTPValidateSerializer, AdminForgotPasswordSetNewSerializer
from .models import OTP
from django.contrib.auth.models import User
# Create your views here.
class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerialisers(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordRequestView(APIView):
    def post(self, request):
        serializer = AdminForgotPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data,{"message": "OTP sent to email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordOTPValidateView(APIView):
    def post(self, request):
        serializer = AdminForgotPasswordOTPValidateSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP validated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordResetView(APIView):
    def post(self,request):
        serializer=AdminForgotPasswordSetNewSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data,{"message": "Password reset successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
