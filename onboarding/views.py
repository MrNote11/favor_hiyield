from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
import csv
from drf_yasg.utils import swagger_auto_schema
from .models import Customeruser
from .serializers import *
from .filter import CustomerUserFilter
from django_filters.rest_framework import DjangoFilterBackend

@swagger_auto_schema(
    request_body=AdminLoginSerializer,
    operation_description="Admin login endpoint",)
class AdminLoginAPIView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful'
            })
        return Response(serializer.errors, status=400)
@swagger_auto_schema(
    request_body=AdminForgotPasswordRequestSerializer,
    operation_description="Request password reset for admin",
)
class AdminForgotPasswordRequestView(APIView):
    def post(self, request):
        serializer = AdminForgotPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'OTP sent to email.'})
        return Response(serializer.errors, status=400)
@swagger_auto_schema(
    request_body=AdminForgotPasswordOTPValidateSerializer,
    operation_description="Validate OTP for admin password reset",
)
class AdminOTPValidateView(APIView):
    def post(self, request):
        serializer = AdminForgotPasswordOTPValidateSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'OTP verified.'})
        return Response(serializer.errors, status=400)
@swagger_auto_schema(
    request_body=AdminForgotPasswordSetNewSerializer,
    operation_description="Set new password for admin",
)
class AdminSetNewPasswordView(APIView):
    def post(self, request):
        serializer = AdminForgotPasswordSetNewSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Password reset successful.'})
        return Response(serializer.errors, status=400)

class CustomerSignupView(CreateAPIView):
    serializer_class = CustomerSignupSerializer
    permission_classes = [permissions.AllowAny]


@swagger_auto_schema(operation_description='all customers view')
class AllCustomersView(ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Customeruser.objects.filter(is_staff=False).order_by('-date_joined')
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerUserFilter
    @swagger_auto_schema(
        operation_description="List all customers with optional CSV download",
    )
    def get(self, request, *args, **kwargs):
        if request.query_params.get('download') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="customers.csv"'
            writer = csv.writer(response)
            writer.writerow(['ID', 'Username', 'Email', 'Date Joined', 'Blacklisted'])
            for user in queryset:
                writer.writerow([user.id, user.username, user.email, user.date_joined, user.blacklist])
            return response
        return super().get(request, *args, **kwargs)

class CustomerUserDetailView(RetrieveAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'
    queryset = Customeruser.objects.filter(is_staff=False)

class BlacklistToggleView(UpdateAPIView):
    """
    Admin-only view to toggle a customer's blacklist status.
    """
    queryset = Customeruser.objects.filter(is_staff=False)
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]
    @swagger_auto_schema(
        operation_description="Toggle blacklist status of a customer",
        responses={200: CustomerSerializer, 404: 'Customer not found'}
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.blacklist = not user.blacklist
        user.save()
        status_text = "blacklisted" if user.blacklist else "unblacklisted"
        return Response({'message': f'Customer has been {status_text}.'})
