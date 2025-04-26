from django.contrib import admin

from .models import Type, Brand, Device


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'rating', 'type', 'brand')
    search_fields = ('title', 'description')
    list_filter = ('type', 'brand')
    ordering = ('id', 'price', 'rating')
