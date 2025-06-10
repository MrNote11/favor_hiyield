from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
import csv
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from .serializers import *
from .models import Customeruser
from .filter import CustomerUserFilter                                                                                                                                                                                                       
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

class AdminLoginAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Admin Login",
        request_body=AdminLoginSerializer,
    )
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user.is_admin:  # or user.is_admin if you use that field
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "Login successful"
                }, status=status.HTTP_200_OK)
            return Response({"error": "Not an admin user"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminForgotPasswordRequestView(APIView):
    def post(self, request):
        serializer = AdminForgotPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'OTP sent to email.'})
        return Response(serializer.errors, status=400)

class AdminOTPValidateView(APIView):
    def post(self, request):
        serializer = AdminForgotPasswordOTPValidateSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'OTP verified.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminSetNewPasswordView(APIView):
    def post(self, request):
        serializer = AdminForgotPasswordSetNewSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Password reset successful.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerSignupView(CreateAPIView):
    serializer_class = CustomerSignupSerializer
    permission_classes = [permissions.AllowAny]


class AllCustomersView(ListAPIView):
    serializer_class = CustomerListSerializer
    queryset = Customeruser.objects.filter(is_admin=False).order_by('-date_joined')
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerUserFilter

    def get(self, request, *args, **kwargs):
        if request.query_params.get('download') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="customers.csv"'
            writer = csv.writer(response)
            writer.writerow(['ID', 'Username', 'Email', 'Date Joined'])
            for user in queryset:
                writer.writerow([user.id, user.username, user.email, user.date_joined])
            return response
        return super().get(request, *args, **kwargs)


class CustomerDetailView(RetrieveAPIView):
    serializer_class = CustomerDetailSerializer
    queryset = Customeruser.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

    def get_object(self):
        return self.request.user
