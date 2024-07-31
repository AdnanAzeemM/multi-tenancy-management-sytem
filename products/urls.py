from django.urls.conf import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, CategoryViewSet, BrandViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename="products")
router.register(r'category', CategoryViewSet, basename="category")
router.register(r'brand', BrandViewSet, basename="brand")

urlpatterns = [
    path('', include(router.urls))
]