from django.db import models


class Type(models.Model):
    """
    Модель категории устройства, например 'Смартфон', 'Ноутбук' и т.д.
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Модель бренда устройства, например 'Apple', 'Samsung' и т.д.
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    """
    Модель устройства, которое продается в магазине.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0)

    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='devices')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='devices')

    def __str__(self):
        return self.title
