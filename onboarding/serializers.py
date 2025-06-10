from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTP
from django.core.mail import send_mail
import os
from dotenv import load_dotenv

load_dotenv()
User = get_user_model()


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email, is_admin=True).first()
        if user and user.check_password(password):
            data['user'] = user
        else:
            raise serializers.ValidationError("Invalid email or password.")
        return data


class AdminForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        user = User.objects.filter(email=email, is_admin=True).first()
        if not user:
            raise serializers.ValidationError("Admin with this email does not exist.")
        self.user = user
        return email

    def create(self, validated_data):
        otp_obj, _ = OTP.objects.get_or_create(user=self.user)
        otp_code = otp_obj.generate_otp()
        send_mail(
            subject='Admin Password Reset OTP',
            message=f'Your OTP is: {otp_code}',
            from_email=os.getenv('EMAIL_HOST_USER'),
            recipient_list=[self.user.email],
        )
        return validated_data


class AdminForgotPasswordOTPValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        user = User.objects.filter(email=data['email'], is_admin=True).first()
        if not user:
            raise serializers.ValidationError("Admin not found.")
        otp_obj = OTP.objects.filter(user=user, otp=data['otp']).first()
        if not otp_obj or otp_obj.is_expired():
            raise serializers.ValidationError("Invalid or expired OTP.")
        return data


class AdminForgotPasswordSetNewSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        user = User.objects.filter(email=data['email'], is_admin=True).first()
        otp_obj = OTP.objects.filter(user=user, otp=data['otp']).first()
        if not user or not otp_obj or otp_obj.is_expired():
            raise serializers.ValidationError("Invalid or expired OTP.")
        
        user.set_password(data['new_password'])
        user.save()
        return data


class CustomerSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_no', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['is_admin'] = False
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user

class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_no', 'date_joined')

class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_no', 'date_joined', 'is_active', 'is_staff')
        read_only_fields = ('id', 'date_joined', 'is_active', 'is_staff')
