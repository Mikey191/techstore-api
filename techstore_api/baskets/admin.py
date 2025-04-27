from django.contrib import admin

from baskets.models import BasketDevice, Basket


class BasketDeviceInline(admin.TabularInline):
    """
    Настройка отображения устройств в корзине
    """
    model = BasketDevice
    extra = 1
    readonly_fields = ('device', 'quantity')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """
    Админка для корзины пользователя
    """
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__email')
    inlines = [BasketDeviceInline]


@admin.register(BasketDevice)
class BasketDeviceAdmin(admin.ModelAdmin):
    """
    Админка для связи корзина-устройства
    """
    list_display = ('id', 'basket', 'device', 'quantity')
    list_filter = ('basket', 'device')
    search_fields = ('basket__user__username', 'device__title')
