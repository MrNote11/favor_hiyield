from django.db.models import Max
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, views, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignUpSuperUserSerializers, LoginSerializer, UserRoleFeatureSerializer, AdminAndCustomerSerializer
from .models import Roles,  CustomUser
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission

class IsSuperUserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser



class CreateUser(viewsets.ModelViewSet):
    serializer_class = SignUpSuperUserSerializers
    permission_classes = [IsSuperUserOnly]
    queryset = CustomUser.objects.all()
    
    

class UserRoleAndFeatureViews(viewsets.ModelViewSet):
    serializer_class = UserRoleFeatureSerializer
    permission_classes = [IsAdminUser]
    queryset = Roles.objects.select_related('admin_user')
    
    

class AdminAndCustomerTotalViews(viewsets.ModelViewSet):
    serializer_class = AdminAndCustomerSerializer
    permission_classes = [IsSuperUserOnly]
    queryset = CustomUser.objects.all()
    

    
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            print(user)
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


