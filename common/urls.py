from django.urls import path, include
from rest_framework.routers import DefaultRouter
from common import views

router = DefaultRouter()

router.register(r'country', views.CountryViewSet, basename="country")
router.register(r'state', views.StateViewSet, basename="state")
router.register(r'city', views.CityViewSet, basename="city")

urlpatterns = [
    path('', include(router.urls)),
]


