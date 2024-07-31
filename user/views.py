from django.http import HttpResponseForbidden
from django.shortcuts import render
from django_tenants.utils import get_tenant_model, get_public_schema_name
from rest_framework import status, generics
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import CustomUser, Client, Domain, Employee
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, EmployeeSerializer
from rest_framework.views import APIView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]


def normalize_business_name(name):
    return name.strip().lower().replace(" ", "")


class CreateSubUserAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        tenant_model = get_tenant_model()
        current_tenant = request.tenant
        if current_tenant:
            schema_name = current_tenant.schema_name.strip().lower().replace(" ", "")
            try:
                domain_user = CustomUser.objects.get(business_name=schema_name)

            except CustomUser.DoesNotExist:
                return None

            user = CustomUser(
                username=validated_data['first_name'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                mobile_number=validated_data['mobile_number'],
                is_mobile_verified=validated_data['is_mobile_verified'],
                # business_name=validated_data['business_name'],
            )
            user.set_password(validated_data['password'])
            user.save()
            employee = Employee(
                user=domain_user.id,
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                mobile_number=validated_data['mobile_number'],
                is_mobile_verified=validated_data['is_mobile_verified'],
                job_title=validated_data['job_title'],
                department=validated_data['department'],

            )
            employee.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EmployeeAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Validate incoming data with the EmployeeSerializer
        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        # Get the current tenant
        current_tenant = getattr(request, 'tenant', None)
        if not current_tenant:
            return Response({"detail": "Tenant not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Normalize the schema_name
        schema_name = current_tenant.schema_name.strip().lower().replace(" ", "")

        # Try to find the domain user
        try:
            # domain_user = CustomUser.objects.get(business_name=schema_name)
            domain_user = CustomUser.objects.get(business_name=current_tenant.schema_name)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Domain user not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create the new CustomUser instance
        user = CustomUser(
            username=validated_data['first_name'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile_number=validated_data['mobile_number'],
            is_mobile_verified=validated_data['is_mobile_verified'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # Create the Employee instance
        employee = Employee(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            job_title=validated_data['job_title'],
            department=validated_data['department'],
            mobile_number=validated_data['mobile_number'],
            is_mobile_verified=validated_data['is_mobile_verified'],
            password=validated_data['password']
        )
        employee.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)