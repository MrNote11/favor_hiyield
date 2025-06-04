from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdminLoginSerialisers,AdminForgotPasswordRequestSerializer, AdminForgotPasswordOTPValidateSerializer, AdminForgotPasswordSetNewSerializer
from .models import OTP
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
class AdminLoginView(APIView):
    @swagger_auto_schema(
        operation_description="Admin Login",
        request_body=AdminLoginSerialisers,
    )
    def post(self, request):
        serializer = AdminLoginSerialisers(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data['email']).first()

            if user and user.check_password(serializer.validated_data['password']) and user.is_staff :
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "Login successful"
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials or not an admin"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ForgotPasswordRequestView(APIView):
    @swagger_auto_schema(
        operation_description="Request Password Reset",
        request_body=AdminForgotPasswordRequestSerializer,
    )
    def post(self, request):
        serializer = AdminForgotPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({**serializer.validated_data,"message": "OTP sent to email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordOTPValidateView(APIView):
    @swagger_auto_schema(
        operation_description="Validate OTP for Password Reset",
        request_body=AdminForgotPasswordOTPValidateSerializer,
    )
    def post(self, request):
        serializer = AdminForgotPasswordOTPValidateSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP validated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordResetView(APIView):
    @swagger_auto_schema(
        operation_description="Set New Password",
        request_body=AdminForgotPasswordSetNewSerializer,
    )
    def post(self,request):
        serializer=AdminForgotPasswordSetNewSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
