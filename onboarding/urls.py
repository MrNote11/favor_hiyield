
from django.urls import path
from . import views

urlpatterns=[
    path('admin/login',views.AdminLoginView.as_view(), name='admin_login'),
    path('forgot-password/',views.ForgotPasswordRequestView.as_view(), name='forgot_password_request'),
    path('forgot-password/verify-otp/', views.ForgotPasswordOTPValidateView.as_view(), name='forgot_password_validate_otp'),
    path('forgot-password/reset/', views.ForgotPasswordResetView.as_view(), name='forgot_password_reset'),
]