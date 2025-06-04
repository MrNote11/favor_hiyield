from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OTP
import os
from dotenv import load_dotenv
import random
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
load_dotenv()



class AdminLoginSerialisers(serializers.ModelSerializer):
    phone_no = serializers.CharField(max_length=15, required=False, allow_blank=True)
    class Meta:
        model = User
        fields = ('email', 'password','phone_no')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, data):
        email= data.get('email')
        phone_no = data.get('phone_no')
        if not email and not phone_no:
            raise serializers.ValidationError("Email or Phone number is required")
        
        user=None
        if email:
            try:
                user=User.objects.filter(email=email).first()
            except:
                raise serializers.ValidationError("Invalid email format")
        elif phone_no:
            try:
                user=User.objects.filter(profile__phone_no=phone_no).first()
            except:
                raise serializers.ValidationError("Incorrect Phone Number")

        return data


User = get_user_model()

class AdminForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")
        self.user = user
        return email

    def create(self, validated_data):
        otp_obj, _ = OTP.objects.get_or_create(user=self.user)
        otp_code = otp_obj.generate_otp() 

        print(f"Generated OTP: {otp_code} for user: {self.user.email}")

        send_mail(
            subject='Password Reset OTP',
            message=f'Your OTP for password reset is: {otp_code}',
            from_email=os.getenv('EMAIL_HOST_USER'),
            recipient_list=[self.user.email],
            fail_silently=False,
        )

        return validated_data
    
class AdminForgotPasswordOTPValidateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")

        otp_obj = OTP.objects.filter(user=user, otp=otp).first()
        if not otp_obj:
            raise serializers.ValidationError("Invalid OTP.")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP has expired.")

        # Optional: Attach user or OTP object to serializer
        self.user = user
        self.otp_obj = otp_obj

        return data


class AdminForgotPasswordSetNewSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6,required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_new_password=serializers.CharField(write_only=True,required=True, min_length=8)

    def validate(self, data):
        email = data.get('email')
        otp= data.get('otp')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise serializers.ValidationError("New password and confirm password do not match.")
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")
        otp_obj = OTP.objects.filter(user=user, otp=otp).first()
        if not otp_obj:
            raise serializers.ValidationError("Invalid OTP.")
        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP has expired.")
        user.set_password(new_password)
        user.save()
        return data
        
            
        



        


