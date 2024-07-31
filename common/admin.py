from django.contrib import admin
from common.models import Country,City, State


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')