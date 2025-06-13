
from django.urls import path
from . import views

urlpatterns=[
    path('admin/login',views.AdminLoginAPIView.as_view(), name='admin_login'),
    path('forgot-password/',views.AdminForgotPasswordRequestView.as_view(), name='forgot_password_request'),
    path('forgot-password/verify-otp/', views.AdminOTPValidateView.as_view(), name='forgot_password_validate_otp'),
    path('forgot-password/reset/', views.AdminSetNewPasswordView.as_view(), name='forgot_password_reset'),
    path('admin/customerusers/', views.AllCustomersView.as_view(), name='customeruser'),
    path('admin/customerusers/<int:pk>', views.CustomerUserDetailView.as_view(), name='customeruser-detail'),
    path('users/', views.CustomerSignupView.as_view(), name='Customer_user_signup'),
]