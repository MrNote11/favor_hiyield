from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path
from .views import CreateUser, LoginView, UserRoleAndFeatureViews, AdminAndCustomerTotalViews, BvnRecordViews


urlpatterns = [
    path('login/', LoginView.as_view())
]

router = DefaultRouter()
router.register(r'createadmins', CreateUser, basename='createsuperuser')
router.register(r'assignusersrolesfeature', UserRoleAndFeatureViews, basename='assign'),
router.register(r'customerandusers', AdminAndCustomerTotalViews, basename='customerandusers')
router.register(r'bvnrecords', BvnRecordViews, basename='bvnrecords')
urlpatterns += router.urls