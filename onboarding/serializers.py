from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OTP
import os
from dotenv import load_dotenv
import random
from django.contrib.auth import get_user_model
from django.core.mail import get_connection,EmailMessage

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
        Admin_user = User.objects.filter(email=email).first()
        if not Admin_user:
            raise serializers.ValidationError("User with this email does not exist.")
        self.Admin_user = Admin_user
        return email

    def create(self, validated_data):
        otp_code = str(random.randint(100000, 999999))
        otp_obj, created = OTP.objects.get_or_create(user=self.user)
        otp_obj.otp = otp_code
        otp_obj.save()

        # Send OTP via email
        connection = get_connection(
            host='smtp.gmail.com',
            port=587,
            username=os.getenv('EMAIL_HOST_USER'),
            password=os.getenv('EMAIL_HOST_PASSWORD'),
            use_tls=True
        )
        email_msg = EmailMessage(
            subject='Your OTP Code',
            body=f'Your OTP is: {otp_code}',
            from_email=os.getenv('EMAIL_HOST_USER'),
            to=[self.Admin_user.email],
            connection=connection
        )
        email_msg.send()

        return {"message": "OTP sent to email."}

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
        data['message'] = "OTP verified."
        return data

class AdminForgotPasswordSetNewSerializer(serializers.Serializer):
    eail = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        new_password = data.get('new_password')
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")
        otp_obj = OTP.objects.filter(user=user, otp=otp).first()
        if not otp_obj:
            raise serializers.ValidationError("Invalid OTP.")
        user.set_password(new_password)
        user.save()
        otp_obj.delete()
        data['message'] = "Password reset successful."
        return data
            
        



        


