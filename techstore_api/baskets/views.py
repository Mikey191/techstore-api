from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from devices.models import Device
from .models import Basket, BasketDevice
from .serializers import BasketSerializer, AddDeviceToBasketSerializer


class BasketDetailView(generics.RetrieveAPIView):
    """
    View для получения корзины пользователя
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BasketSerializer

    def get_object(self):
        basket, created = Basket.objects.get_or_create(user=self.request.user)
        return basket


class AddDeviceToBasketView(generics.GenericAPIView):
    """
    View для добавления устройства в корзину
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddDeviceToBasketSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device_id = serializer.validated_data['device_id']
        quantity = serializer.validated_data['quantity']

        basket, created = Basket.objects.get_or_create(user=request.user)
        device = Device.objects.get(id=device_id)

        basket_device, created = BasketDevice.objects.get_or_create(basket=basket, device=device)
        if not created:
            basket_device.quantity += quantity
            basket_device.save()
        else:
            basket_device.quantity = quantity
            basket_device.save()

        return Response({'message': 'Device added to basket successfully.'}, status=status.HTTP_200_OK)


class RemoveDeviceFromBasketView(generics.DestroyAPIView):
    """
    View для удаления устройства из корзины
    """

    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'basket_device_id'

    def delete(self, request, *args, **kwargs):
        basket_device_id = kwargs.get(self.lookup_url_kwarg)
        basket = Basket.objects.filter(user=request.user).first()

        if not basket:
            return Response({'error': 'Basket not found.'}, status=status.HTTP_404_NOT_FOUND)

        basket_device = BasketDevice.objects.filter(id=basket_device_id, basket=basket).first()
        if not basket_device:
            return Response({'error': 'Device not found in your basket.'}, status=status.HTTP_404_NOT_FOUND)

        basket_device.delete()
        return Response({'message': 'Device removed from basket successfully.'}, status=status.HTTP_200_OK)
