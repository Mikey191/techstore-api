from django.conf import settings
from django.db import models

from devices.models import Device


class Basket(models.Model):
    """
    Модель корзины пользователя
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket'
    )

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'


class BasketDevice(models.Model):
    """
    Промежуточная корзина пользователя
    """
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name='basket_devices'
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='basket_devices'
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.device.title} (x {self.quantity}) в корзине {self.basket.user.username}"
