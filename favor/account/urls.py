from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path
from .views import CreateUser, LoginView, UserRoleAndFeatureViews, AdminAndCustomerTotalViews


urlpatterns = [
    path('login/', LoginView.as_view())
]

router = DefaultRouter()
router.register(r'createsuperadmin', CreateUser, basename='createsuperuser')
router.register(r'assignusersrolesfeature', UserRoleAndFeatureViews, basename='assign'),
router.register(r'customersandusers', AdminAndCustomerTotalViews, basename='customerandusers')
urlpatterns += router.urls