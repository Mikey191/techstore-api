from rest_framework import serializers

from baskets.models import BasketDevice, Basket
from devices.models import Device


class BasketDeviceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для устройств в корзине
    """

    device_title = serializers.CharField(source='device.title', read_only=True)
    device_price = serializers.DecimalField(source='device.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = BasketDevice
        fields = ['id', 'device', 'device_title', 'device_price', 'quantity']
        read_only_fields = ['id', 'device_title', 'device_price']


class BasketSerializer(serializers.ModelSerializer):
    """
    Сериализатор для полной информации о корзине
    """
    devices = BasketDeviceSerializer(source='basket_devices', many=True, read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'devices']
        read_only_fields = ['id', 'user', 'devices']


class AddDeviceToBasketSerializer(serializers.Serializer):
    """
    Сериализатор для добавления устройства в корзину
    """
    device_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_device_id(self, value):
        if not Device.objects.filter(id=value).exists():
            raise serializers.ValidationError('Device with given ID does not exist.')
        return value
