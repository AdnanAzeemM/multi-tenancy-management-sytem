from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from products.models import Product, Category, Brand
from products.serializers import ProductSerializer, CategorySerializer, BrandSerializer
from rest_framework.permissions import IsAuthenticated
from urllib.parse import urlparse


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]



class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



