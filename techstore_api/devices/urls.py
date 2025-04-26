from django.urls import path

from .views import TypeListCreateAPIView, TypeRetrieveUpdateDestroyAPIView
from .views import BrandListCreateAPIView, BrandRetrieveUpdateDestroyAPIView
from .views import DeviceListCreateAPIView, DeviceRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('types/', TypeListCreateAPIView.as_view(), name='type-list-create'),
    path('types/<int:pk>/', TypeRetrieveUpdateDestroyAPIView.as_view(), name='type-detail'),
    path('brands/', BrandListCreateAPIView.as_view(), name='brand-list-create'),
    path('brands/<int:pk>/', BrandRetrieveUpdateDestroyAPIView.as_view(), name='brand-detail'),
    path('devices/', DeviceListCreateAPIView.as_view(), name='device-list-create'),
    path('devices/<int:pk>/', DeviceRetrieveUpdateDestroyAPIView.as_view(), name='device-detail')
]