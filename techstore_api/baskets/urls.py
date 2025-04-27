from django.urls import path
from .views import AddDeviceToBasketView, RemoveDeviceFromBasketView, BasketDetailView

urlpatterns = [
    path('basket/', BasketDetailView.as_view(), name='basket-detail'),
    path('basket/add/', AddDeviceToBasketView.as_view(), name='basket-add-device'),
    path('basket/remove/<int:basket_device_id>/', RemoveDeviceFromBasketView.as_view(), name='basket-remove-device'),
]