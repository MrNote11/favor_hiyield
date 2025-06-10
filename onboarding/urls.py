
from django.urls import path
from . import views

urlpatterns=[
    path('admin/login',views.AdminLoginAPIView.as_view(), name='admin_login'),
    path('forgot-password/',views.AdminForgotPasswordRequestView.as_view(), name='forgot_password_request'),
    path('forgot-password/verify-otp/', views.AdminOTPValidateView.as_view(), name='forgot_password_validate_otp'),
    path('forgot-password/reset/', views.AdminSetNewPasswordView.as_view(), name='forgot_password_reset'),
    path('admin/users-list/', views.AllCustomersView.as_view(), name='admin_user_list'),
    path('admin/users-list/<int:pk>', views.CustomerDetailView.as_view(), name='admin_user_detail'),
    path('users/', views.CustomerSignupView.as_view(), name='Customer_user_signup'),
]