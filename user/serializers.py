from django.contrib.auth.password_validation import validate_password
from django.dispatch import Signal
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import CustomUser, Client, Domain, Employee


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'mobile_number', 'is_mobile_verified',
                  'business_name', 'password', ]

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile_number=validated_data['mobile_number'],
            is_mobile_verified=validated_data['is_mobile_verified'],
            business_name=validated_data['business_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        if user.business_name:
            business_name = user.business_name.strip().lower().replace(" ", "")

            tenant = Client(
                schema_name=business_name,
                name=user.business_name,
            )
            tenant.save()

            domain = Domain(
                domain=f'{business_name}.localhost', tenant=tenant, is_primary=True
            )
            domain.save()

        return user


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'user', 'first_name', 'last_name', 'email', 'job_title', 'department',
            "mobile_number", "is_mobile_verified", "password"
        ]

