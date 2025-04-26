from rest_framework import serializers
from .models import Type, Brand, Device


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class DeviceSerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    type_id = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all(),
        source='type',
        write_only=True
    )
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        source='brand',
        write_only=True
    )

    class Meta:
        model = Device
        fields = [
            'id',
            'title',
            'description',
            'price',
            'rating',
            'type',
            'brand',
            'type_id',
            'brand_id'
        ]
