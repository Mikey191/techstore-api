# Приложение `TechstoreApi`

# Сущности и их поля

## **Пользователь (User)**. Хранит данные о зарегистрированных пользователях.

- `id` – первичный ключ (PK)
- `username` – имя пользователя
- `email` – электронная почта (уникальное поле)
- `password` – хешированный пароль
- `role` – роль пользователя (например, "admin", "customer")

## **Корзина (Basket)**. Привязана к конкретному пользователю.

- `id` – первичный ключ (PK)
- `user` – внешний ключ (FK) на User

## **Устройство (Device)**. Содержит информацию о товарах.

- `id` – первичный ключ (PK)
- `title` – название устройства
- `description` – описание
- `price` – цена
- `rating` – средний рейтинг устройства
- `type` – внешний ключ (FK) на Type
- `brand` – внешний ключ (FK) на Brand

## **Связь "Корзина - Устройство" (BasketDevice)**. Промежуточная таблица для связи корзины и товаров.

- `id` – первичный ключ (PK)
- `basket` – внешний ключ (FK) на Basket
- `device` – внешний ключ (FK) на Device

## **Оценка (Rating)**. Позволяет пользователям оставлять оценки устройствам.

- `id` – первичный ключ (PK)
- `user` – внешний ключ (FK) на User
- `device` – внешний ключ (FK) на Device
- `rate` – оценка (1-5)

## **Тип устройства (Type)**. Категория товара (например, смартфоны, ноутбуки).

- `id` – первичный ключ (PK)
- `name` – название типа

## **Бренд (Brand)**. Производитель устройства (например, Apple, Samsung).

- `id` – первичный ключ (PK)
- `name` – название бренда

# Структура приложения

```bash
techstore_api/
│── manage.py
│── techstore_api/  # Основной конфиг Django
│
├── users/  # Приложение для пользователей
│   ├── models.py  # User
│   ├── views.py  # Регистрация, авторизация
│   ├── serializers.py  # DRF-сериализаторы
│   ├── urls.py  # API-маршруты
│
├── devices/  # Приложение для работы с товарами
│   ├── models.py  # Device, Brand, Type
│   ├── views.py  # CRUD для устройств
│   ├── serializers.py  # DRF-сериализаторы
│   ├── urls.py  # API-маршруты
│
├── baskets/  # Приложение для корзины
│   ├── models.py  # Basket, BasketDevice
│   ├── views.py  # Логика добавления/удаления
│   ├── serializers.py  # DRF-сериализаторы
│   ├── urls.py  # API-маршруты
│
├── ratings/  # Приложение для оценок
│   ├── models.py  # Rating
│   ├── views.py  # CRUD для оценок
│   ├── serializers.py  # DRF-сериализаторы
│   ├── urls.py  # API-маршруты
```

# Порядок работы над приложениями

## 1. Создание моделей (models.py)

- Определяешь **классы моделей**
- Связываешь через `ForeignKey`, `OneToOneField`, ManyTo`ManyField, если нужно
- Обязательно реализуешь `__str__` для читабельности

## 2. Регистрация моделей в админке (admin.py)

- Регистрируешь модель через `admin.site.register()`
- При необходимости кастомизируешь отображение (`list_display`, `search_fields`, `readonly_fields` и т.д.)

## 3. Создание и применение миграций

```bash
python manage.py makemigrations <название_приложения>
python manage.py migrate
```

## 4. Создание сериализаторов (serializers.py)

- Описываешь **сериализаторы** для моделей
- В случае вложенных данных (например, у устройства есть бренд и тип) — используешь **вложенные сериализаторы** (Nested Serializer)

## 5. Создание представлений (views.py)

- Если простая `CRUD-операция` — используешь `ModelViewSet` или `GenericAPIView`
- Если нужно что-то `кастомное` — пишешь `собственные методы` (`post`, `get`, `put`, `delete`)
- Для `авторизации`/`регистрации` — **отдельные классы** представлений

## 6. Прописание эндпоинтов (urls.py)

- Прописываешь `urlpatterns`
- Подключаешь через `router` для `ViewSet'ов`
- Или через `path()` для функций/классов с базовым `APIView`
- В основном роутере (`techstore_api/urls.py`) подключаешь все мини-роуты приложения

## ✨ Что ещё важно добавить:

- `permissions.py`: Ограничение доступа к эндпоинтам по ролям (IsAdminUser, кастомные права)
- `pagination.py`: Кастомная пагинация для списков
- `filters.py`: Фильтрация по полям (например, устройства по бренду/типу)
- `validators.py`: Валидация полей, если нужно что-то специфичное
- `utils.py`: Вспомогательные функции, если проект начнёт разрастаться

# 1. Создание проекта и настройка базового окружения

## 1. Создать виртуальное окружение и активировать его

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

## 2. Установить Django и Django Rest Framework

```bash
pip install django djangorestframework
```

## 3. Создать проект techstore_api

```bash
django-admin startproject techstore_api
cd techstore_api
```

## 4. Создать первое приложение users

```bash
python manage.py startapp users
```

## 5. Настроить проект (techstore_api/settings.py)

Добавить приложения в INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'users',
]
```

## 6. Настроить базовую авторизацию (если планируешь JWT, пока просто добавить DRF настройки)

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

## 7. Подключить базовые роуты (techstore_api/urls.py)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  # Подключаем роуты пользователей
]
```

# 2. Создание `users`

## 1. Модель пользователя (users/models.py)

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Расширяем стандартную модель пользователя
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username
```

- Наследуемся от `AbstractUser`, чтобы использовать уже готовую авторизацию.
- Добавляем новое поле `role`.
- `__str__` определяем для красивого отображения имени в админке.

## 2. Регистрация модели в админке (users/admin.py)

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Расширяем стандартную админку
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
```

- Расширяем стандартную `админ-панель` пользователя.
- Добавляем отображение роли (`role`) в списке пользователей.

## 3. Создание и применение миграций

В `settings.py` укажи свою кастомную модель пользователя:

```python
AUTH_USER_MODEL = 'users.User'
```

Далее команды в терминале:

```bash
python manage.py makemigrations users
python manage.py migrate
```

- Без `AUTH_USER_MODEL` всё упадёт — Django должен знать о новой модели до первой миграции.
- Миграции создадут таблицу пользователей.

## 4. Создание сериализатора (users/serializers.py)

```python
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        # Хэшируем пароль правильно через create_user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'customer')  # Если роль не указана - ставим customer
        )
        return user
```

- password скрываем через `write_only`.
- При создании пользователя пароль хэшируется через `create_user()`.

## 5. Создание представлений (users/views.py)

```python
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny

class UserRegisterView(generics.CreateAPIView):
    """
    Представление для регистрации нового пользователя.
    Доступно всем без авторизации.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
```

- Используем `CreateAPIView` для регистрации новых пользователей.
- `AllowAny` — доступ открыт всем (иначе зарегистрироваться будет нельзя без токена).

## 6. Прописание эндпоинтов (users/urls.py)

```python
from django.urls import path
from .views import UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
]
```

- Создаём роут `/api/users/register/`
- Через него будет проходить регистрация новых пользователей.

## 7. Добавление логина с использованием `JWT`

### Установить библиотеку Simple JWT

```bash
pip install djangorestframework-simplejwt
```

### Настроить аутентификацию в settings.py

Добавить настройки для `SimpleJWT`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

- Теперь всё приложение по умолчанию требует авторизацию по JWT токену.

### Добавить URL-маршруты для логина/обновления токена (users/urls.py)

Расширяем `urls.py` в приложении users:

```python
Копировать
Редактировать
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),  # Логин
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),  # Обновление токена
]
```

- `/api/users/login/` — для получения `access` и `refresh` токенов.
- `/api/users/refresh/` — для обновления `access` токена, если старый истёк.

### (Необязательно) Кастомизация ответа при логине

Можно дополнить стандартный логин-эндпоинт своим выводом. Например, чтобы возвращать ещё и роль пользователя.

#### Создадим свой сериализатор:

```python
# users/serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавляем кастомные данные в payload токена
        token['username'] = user.username
        token['role'] = user.role

        return token
```

#### Своё представление:

```python
# users/views.py

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```

#### В users/urls.py нужно поменять импорт:

```python
from .views import UserRegisterView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),  # Наш кастомный логин
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
```

Теперь токен будет содержать ещё `username` и `role` — это удобно на фронте для быстрого понимания, кто вошёл.

### Как пользоваться

#### **Для регистрации: POST /api/users/register/**

**тело запроса**:

```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "secret123",
  "role": "customer"
}
```

#### **Для логина: POST /api/users/login/**

**тело запроса**:

```json
{
  "username": "newuser",
  "password": "secret123"
}
```

**ответ**:

```json
{
  "refresh": "long_refresh_token_here",
  "access": "short_access_token_here"
}
```

#### **Для обновления токена: POST /api/users/refresh/**

**тело запроса**:

```json
{
  "refresh": "long_refresh_token_here"
}
```

**ответ**:

```json
{
  "access": "new_short_access_token_here"
}
```

## 8. Получение профиля текущего пользователя `/me/

### Добавить сериализатор для просмотра профиля

```python
# users/serializers.py

from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения профиля текущего пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')
```

- Мы не возвращаем пароль и никакие лишние данные.

### Добавить вьюшку для получения данных текущего пользователя

```python
# users/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from .models import User

class UserProfileView(generics.RetrieveAPIView):
    """Представление для получения данных текущего пользователя."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Возвращаем текущего пользователя
        return self.request.user
```

- `RetrieveAPIView` — стандартная вьюшка для получения одного объекта.
- `get_object()` возвращает пользователя, который сделал запрос по токену.
- Никаких запросов типа `User.objects.get(pk=self.request.user.id)` — данные берутся напрямую из `request.user`, который `DRF` автоматически подтягивает при проверке токена.

### Добавить эндпоинт в users/urls.py

```python
from .views import UserRegisterView, CustomTokenObtainPairView, UserProfileView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
]
```

### Как пользоваться `/me/`

#### **Запрос: `GET /api/users/me/`**

- Заголовок: `Authorization: Bearer <access_token>`

- Ответ пример:

```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "role": "customer"
}
```

- Без токена вернёт 401 (Unauthorized).
- Никаких ID в URL — всё автоматически определяется на основе авторизации!

# 3. Создание `devices`

## 1. 📄 devices/models.py

```python
from django.db import models

class Type(models.Model):
    """
    Модель категории устройства, например 'Смартфон', 'Ноутбук' и т.д.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    # Для удобного отображения в админке и в консоли будет выводиться название типа


class Brand(models.Model):
    """
    Модель бренда устройства, например 'Apple', 'Samsung' и т.д.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    # Аналогично — для красивого вывода имени бренда


class Device(models.Model):
    """
    Модель устройства, которое продается в магазине.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Описание можно оставить пустым
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0)  # Средний рейтинг устройства (по умолчанию 0)

    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='devices')
    # Внешний ключ на таблицу Type (категория устройства)
    # Если удалится категория — все устройства этой категории тоже удалятся

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='devices')
    # Внешний ключ на таблицу Brand (бренд устройства)
    # При удалении бренда также удаляются устройства этого бренда

    def __str__(self):
        return self.title
    # При выводе устройства будет показываться его заголовок
```

### Комментарии

- `name в Type и Brand`: unique=True, чтобы не было двух типов или брендов с одинаковыми названиями.
- `price`: Используем DecimalField, а не FloatField, потому что цена требует высокой точности (особенно для финансов).
- `rating`: Плавающее число от 0 до 5 (будем обновлять при новых оценках).
- `ForeignKey`: Настроен с on_delete=models.CASCADE, чтобы связанные устройства удалялись вместе с категорией или брендом.
- `related_name='devices'`: Это позволяет потом удобно обращаться к устройствам типа или бренда (some_type.devices.all()).

## 2. Регистрация моделей в админке `devices/admin.py`

```python
# devices/admin.py

from django.contrib import admin
from .models import Type, Brand, Device

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Какие поля будут отображаться в списке в админке
    search_fields = ('name',)      # По каким полям можно искать
    ordering = ('id',)             # Сортировка по id

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'rating', 'type', 'brand')
    search_fields = ('title', 'description')
    list_filter = ('type', 'brand')  # Фильтрация по типу и бренду
    ordering = ('id',)
```

### Объяснение

- `@admin.register(...)`: Удобный современный способ регистрации моделей вместо admin.site.register().
- `list_display`: Управляем, какие поля будут показываться в списке объектов в админке.
- `search_fields`: Позволяет искать объекты по указанным полям через панель поиска.
- `list_filter`: Фильтрация справа в админке по выбранным полям (например, быстро выбрать устройства определенного бренда).
- `ordering`: Стандартная сортировка записей в списке.

## 3. Создание миграций

### Добавить приложение в настройках settings.py

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'users',
    'devices'
]
```

### Создание миграций

```bash
python manage.py makemigrations devices
```

- Команда создаст файл миграции для приложения `devices/`.
- Он будет содержать инструкции, как создать таблицы для `Type`, `Brand`, `Device`.

### Применение миграций

```bash
python manage.py migrate
```

- Теперь таблицы реально создадутся в базе данных.

## 4. Создание сериализаторов

```python
# devices/serializers.py
from rest_framework import serializers
from .models import Type, Brand, Device

# Сериализатор для модели Type
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']  # Явно указываем, какие поля хотим сериализовать

# Сериализатор для модели Brand
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

# Сериализатор для модели Device
class DeviceSerializer(serializers.ModelSerializer):
    # Чтобы вместо id-шников выводить нормальные данные о типе и бренде
    type = TypeSerializer(read_only=True)  # Вложенный сериализатор
    brand = BrandSerializer(read_only=True)

    # Чтобы при создании передавать именно id-шники (а не всё тело вложенных объектов)
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
```

### Объяснение

- **Созданы сериализаторы `TypeSerializer` и `BrandSerializer`**: Чтобы управлять сериализацией моделей Type и Brand отдельно.
- **В `DeviceSerializer` добавлены вложенные сериализаторы (`TypeSerializer` и `BrandSerializer`)**: Чтобы в ответе API видеть всю информацию о типе и бренде, а не только их id.
- **Добавлены поля `type_id` и `brand_id`**: Чтобы при создании/обновлении устройства в запросе можно было отправлять только id типа и бренда, а не весь объект.
- **`source='type'` и `source='brand'`**: Указываем, что эти поля маппятся на реальные связи модели Device.

### Как теперь будет выглядеть JSON устройства через API?

#### Ответ от сервера при получении устройства:

```json
{
  "id": 5,
  "title": "iPhone 15",
  "description": "Новейший iPhone 15 от Apple",
  "price": 999.99,
  "rating": 4.8,
  "type": {
    "id": 1,
    "name": "Смартфоны"
  },
  "brand": {
    "id": 2,
    "name": "Apple"
  }
}
```

#### Запрос на создание устройства (POST):

```json
{
  "title": "Galaxy S24",
  "description": "Флагман Samsung",
  "price": 899.99,
  "rating": 4.7,
  "type_id": 1,
  "brand_id": 3
}
```

## 5. Создание `views` для работы с типами, брендами и устройствами

```python
# devices/views.py
from rest_framework import generics
from .models import Type, Brand, Device
from .serializers import TypeSerializer, BrandSerializer, DeviceSerializer

# === Views для Type ===

# Получение списка всех типов и создание нового
class TypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

# Получение, обновление и удаление одного типа по id
class TypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

# === Views для Brand ===

# Получение списка всех брендов и создание нового
class BrandListCreateAPIView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# Получение, обновление и удаление одного бренда по id
class BrandRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# === Views для Device ===

# Получение списка всех устройств и создание нового устройства
class DeviceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

# Получение, обновление и удаление одного устройства по id
class DeviceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
```

### Объяснение

- `ListCreateAPIView`: Позволяет получить список всех объектов и создать новый. Автоматически обрабатывает методы GET и POST.
- `RetrieveUpdateDestroyAPIView`: Позволяет получить объект по id, изменить его (PUT/PATCH) или удалить (DELETE).

## 6. Настроить маршруты (urls.py) для всех views.

```python
# devices/urls.py

from django.urls import path
from .views import (
    TypeListCreateAPIView, TypeRetrieveUpdateDestroyAPIView,
    BrandListCreateAPIView, BrandRetrieveUpdateDestroyAPIView,
    DeviceListCreateAPIView, DeviceRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    # === Типы устройств (Type) ===
    path('types/', TypeListCreateAPIView.as_view(), name='type-list-create'),  # GET, POST
    path('types/<int:pk>/', TypeRetrieveUpdateDestroyAPIView.as_view(), name='type-detail'),  # GET, PUT/PATCH, DELETE

    # === Бренды устройств (Brand) ===
    path('brands/', BrandListCreateAPIView.as_view(), name='brand-list-create'),  # GET, POST
    path('brands/<int:pk>/', BrandRetrieveUpdateDestroyAPIView.as_view(), name='brand-detail'),  # GET, PUT/PATCH, DELETE

    # === Устройства (Device) ===
    path('devices/', DeviceListCreateAPIView.as_view(), name='device-list-create'),  # GET, POST
    path('devices/<int:pk>/', DeviceRetrieveUpdateDestroyAPIView.as_view(), name='device-detail'),  # GET, PUT/PATCH, DELETE
]
```

### Подключение к основному проекту

```python
# techstore_api/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),      # Пользователи
    path('api/', include('devices.urls')),    # Устройства, бренды, типы
]
```

### Как это будет работать

```
/api/types/	            GET	            Получить все типы
/api/types/	            POST	        Создать новый тип
/api/types/<id>/	    GET	            Получить тип по id
/api/types/<id>/	    PUT/PATCH	    Обновить тип
/api/types/<id>/	    DELETE	        Удалить тип
/api/brands/	        GET/POST	    То же самое для брендов
/api/devices/	        GET/POST	    То же самое для устройств
```

# 4. Создание `baskets`

## 1. 📄 `baskets/models.py`

```python
from django.db import models
from django.conf import settings
from devices.models import Device  # Импортируем модель устройств

# === Модель Корзины пользователя ===
class Basket(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Ссылка на модель пользователя
        on_delete=models.CASCADE,  # При удалении пользователя - удаляется корзина
        related_name='basket'      # Позволяет из пользователя получить его корзину: user.basket
    )

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

# === Промежуточная модель "Корзина - Устройства" ===
class BasketDevice(models.Model):
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name='basket_devices'  # Доступ к устройствам корзины: basket.basket_devices.all()
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='basket_devices'  # Устройства могут быть в разных корзинах
    )
    quantity = models.PositiveIntegerField(default=1)  # Количество одного товара в корзине

    def __str__(self):
        return f'{self.device.title} (x{self.quantity}) в корзине {self.basket.user.username}'
```

### Объяснение:

- `Basket`:
  - Привязывается Один к одному (`OneToOne`) к пользователю.
  - **Логика**: у каждого пользователя своя личная корзина.
  - Если пользователь удаляется — его корзина удаляется тоже (`CASCADE`).
- `BasketDevice`:
  - **Связывает корзину и устройство** (многие ко многим через промежуточную модель).
  - Можно хранить **количество товара** (`quantity`), чтобы, например, заказать сразу 3 телефона.
- Мы сразу добавили нормальные `__str__` методы, чтобы было красиво видно записи в админке.

### Почему в модели `Basket` связь с пользователем через `OneToOneField`?

```python
user = models.OneToOneField(User, on_delete=models.CASCADE)
```

- **Что это значит**:
  - **Один пользователь может иметь только одну корзину**. (🧺 `1 Basket = 1 User`)
  - И наоборот — **каждая корзина принадлежит только одному пользователю**.
- **Отличие от `ForeignKey`**:
  - `ForeignKey` создает связь `"много к одному" `(один пользователь может иметь много корзин).
  - `OneToOneField` создает `"один к одному"` (одна корзина на одного пользователя и всё).
- **Почему так сделано для корзины**:
  - **Логика интернет-магазина**: у пользователя должна быть одна активная корзина, куда он складывает товары.
  - **Нет смысла позволять одному юзеру иметь несколько разных корзин одновременно** (если бы были "отложенные корзины" или "список желаний" — тогда можно было бы сделать ForeignKey).

### 🔵 Схема:

```bash
User 1 — 1 Basket
Basket 1 — N BasketDevice
BasketDevice 1 — 1 Device
```

## 2. Добавить `baskets` в `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'baskets',
]
```

## 3. Создать миграции:

```bash
python manage.py makemigrations baskets
python manage.py migrate
```

## 4. Оформляем `админку` для приложения `baskets`

```python
# baskets/admin.py

from django.contrib import admin
from .models import Basket, BasketDevice

# === Настройка отображения устройств в корзине ===
class BasketDeviceInline(admin.TabularInline):
    model = BasketDevice
    extra = 1  # Количество пустых форм для добавления новых товаров
    readonly_fields = ('device', 'quantity')  # Только для просмотра в корзине, без изменения

# === Админка для корзины пользователя ===
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')  # Какие поля показывать в списке
    search_fields = ('user__username', 'user__email')  # Поиск по имени пользователя и почте
    inlines = [BasketDeviceInline]  # Показываем устройства в корзине прямо внутри корзины

# === Админка для связи корзина-устройства ===
@admin.register(BasketDevice)
class BasketDeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'basket', 'device', 'quantity')  # Какие поля отображать
    list_filter = ('basket', 'device')  # Возможность фильтрации
    search_fields = ('basket__user__username', 'device__title')  # Поиск по пользователю и устройству
```

### Объяснение:

- `BasketDeviceInline`:
  - Это `"встроенная таблица"` товаров внутри корзины.
  - Когда заходишь в корзину пользователя — сразу видишь, что у него лежит.
- `BasketAdmin`:
  - В списке корзин показываем `ID` и `пользователя`.
  - Можно искать корзины по `имени` или `почте` пользователя.
  - Устройства в корзине показываются через `inlines`.
- `BasketDeviceAdmin`:
  - Если нужно отдельно работать со связями корзина-товар — доступна отдельная вкладка.
  - Можно искать по названию устройства или по пользователю корзины.

## 5. Оформим `сериализаторы` для работы с корзиной

```python
# baskets/serializers.py

from rest_framework import serializers
from .models import Basket, BasketDevice
from devices.models import Device  # Чтобы подтянуть данные о товарах

# === Сериализатор для устройств в корзине ===
class BasketDeviceSerializer(serializers.ModelSerializer):
    device_title = serializers.CharField(source='device.title', read_only=True)
    device_price = serializers.DecimalField(source='device.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = BasketDevice
        fields = ['id', 'device', 'device_title', 'device_price', 'quantity']
        read_only_fields = ['id', 'device_title', 'device_price']

# === Сериализатор для полной информации о корзине ===
class BasketSerializer(serializers.ModelSerializer):
    devices = BasketDeviceSerializer(source='basket_devices', many=True, read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'devices']
        read_only_fields = ['id', 'user', 'devices']

# === Сериализатор для добавления устройства в корзину ===
class AddDeviceToBasketSerializer(serializers.Serializer):
    device_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_device_id(self, value):
        # Проверяем, что устройство существует
        from devices.models import Device
        if not Device.objects.filter(id=value).exists():
            raise serializers.ValidationError('Device with given ID does not exist.')
        return value
```

### Объяснение:

- `BasketDeviceSerializer`:
  - **Отвечает за отображение информации об одном устройстве в корзине**.
  - Автоматически показывает **название** и **цену** устройства (`read_only`).
- `BasketSerializer`:
  - **Отображает корзину с пользователем и всеми его устройствами**.
  - Подключает к корзине все связанные объекты `BasketDevice`.
- `AddDeviceToBasketSerializer`:
  - **Специальный сериализатор для добавления товара в корзину через `API`**.
  - Позволяет передать `device_id` и `quantity`.
  - При валидации проверяет, существует ли устройство с таким `ID`.

### Разбор кода `BasketSerializer` и `BasketDeviceSerializer`

#### 📄 `BasketDeviceSerializer`:

```python
class BasketDeviceSerializer(serializers.ModelSerializer):
    device_title = serializers.CharField(source='device.title', read_only=True)
    device_price = serializers.DecimalField(source='device.price', max_digits=10, decimal_places=2, read_only=True)
```

- **Что делает**:
  - `device_title`: **показывает название устройства прямо в ответе** (чтобы не приходилось руками доставать device.id и еще один запрос делать).
  - `device_price`: **показывает цену устройства**.
- **Параметры**:
  - `source='device.title'` — говорит сериализатору: **"бери поле `title` у связанного объекта `device`"**.
  - `read_only=True` — **поле доступно только на чтение**, пользователь его не может изменить через API.
- **fields**:
  - `id` — **id записи в таблице `BasketDevice`**
  - `device` — **id устройства**
  - `device_title` — **название устройства**
  - `device_price` — **цена устройства**
  - `quantity` — **количество единиц устройства в корзине**

#### 📄 BasketSerializer:

```python
class BasketSerializer(serializers.ModelSerializer):
    devices = BasketDeviceSerializer(source='basket_devices', many=True, read_only=True)
```

- **Что делает**:
  - **В корзине показываются все устройства** (BasketDevice), которые в ней есть.
- **Параметры**:
  - `source='basket_devices'` — переопределил стандартное имя `basketdevice_set`. Когда у `ForeignKey` указан related_name, то Django больше НЕ создаёт `basketdevice_set`. **Он создает то, что ты явно написал**.
  - `many=True` — **потому что у одной корзины может быть много товаров**.
  - `read_only=True` — **пользователь не может менять список товаров через этот сериализатор** (только через отдельные запросы на добавление/удаление).
- **fields**:
  - `id` — **id корзины**
  - `user` — **пользователь** (id)
  - `devices` — **список устройств в корзине** (используя BasketDeviceSerializer)

#### 📄 AddDeviceToBasketSerializer:

```python
class AddDeviceToBasketSerializer(serializers.Serializer):
    device_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
```

- **Что делает**:
  - **Принимает на вход **`device_id` и `quantity`.
  - Проверяет, **существует ли устройство**.
- **Параметры**:
  - `device_id` — **ID устройства, которое хотим добавить в корзину**.
  - `quantity` — **сколько штук хотим положить**.
  - `validate_device_id` — кастомная проверка: **если такого устройства нет, ошибка**.

## 6. Опишем `views` для работы с корзиной: `просмотр содержимого`, `добавление устройства` и `удаление устройства`.

```python
# baskets/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Basket, BasketDevice
from devices.models import Device
from .serializers import BasketSerializer, BasketDeviceSerializer, AddDeviceToBasketSerializer

# === View для получения корзины пользователя ===
class BasketDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BasketSerializer

    def get_object(self):
        # Ищем корзину текущего пользователя, если нет - создаём
        basket, created = Basket.objects.get_or_create(user=self.request.user)
        return basket

# === View для добавления устройства в корзину ===
class AddDeviceToBasketView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddDeviceToBasketSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device_id = serializer.validated_data['device_id']
        quantity = serializer.validated_data['quantity']

        basket, created = Basket.objects.get_or_create(user=request.user)
        device = Device.objects.get(id=device_id)

        # Проверяем, есть ли уже такое устройство в корзине
        basket_device, created = BasketDevice.objects.get_or_create(basket=basket, device=device)
        if not created:
            # Если уже есть, увеличиваем количество
            basket_device.quantity += quantity
            basket_device.save()
        else:
            # Иначе сохраняем с переданным количеством
            basket_device.quantity = quantity
            basket_device.save()

        return Response({'message': 'Device added to basket successfully.'}, status=status.HTTP_200_OK)

# === View для удаления устройства из корзины ===
class RemoveDeviceFromBasketView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'basket_device_id'  # Параметр в URL

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
```

### Объяснение:

- `BasketDetailView`:
  - **Возвращает полную корзину пользователя** (список всех товаров).
  - **Если корзины нет — создаёт новую пустую корзину автоматически**.
- `AddDeviceToBasketView`:
  - Принимает `device_id` и `quantity`.
  - **Если устройство уже есть в корзине — увеличивает количество**.
  - **Если нет — добавляет новое устройство в корзину**.
- `RemoveDeviceFromBasketView`:
  - **Удаляет конкретное устройство** из корзины по его `basket_device_id`.
  - Защита: **удалять можно только свои устройства**.

### Подробный разбор `BasketDetailView`, `AddDeviceToBasketView`, `RemoveDeviceFromBasketView`

#### 📄 `BasketDetailView`

```python
basket, created = Basket.objects.get_or_create(user=self.request.user)
```

- **Что делает**:
  - **Ищет корзину пользователя по его `user_id`**.
  - **Если корзины нет, автоматически создает новую пустую корзину для этого пользователя**.
  - _Это гарантирует, что каждый юзер всегда имеет актуальную корзину при первом запросе_.
- **Возвращает**:
  - **Корзину, чтобы отдать её сериализованную через `BasketSerializer`**.

#### 📄 `AddDeviceToBasketView`. Что происходит в методе post:

- **Валидация запроса**:

  ```python
  serializer = self.get_serializer(data=request.data)
  serializer.is_valid(raise_exception=True)
  ```

  - Проверяем, что переданы корректные `device_id` и `quantity`.

- **Извлечение данных**:

  ```python
  device_id = serializer.validated_data['device_id']
  quantity = serializer.validated_data['quantity']
  ```

- **Получение или создание корзины**:

  ```python
  basket, created = Basket.objects.get_or_create(user=request.user)
  ```

- **Получение устройства по `id`**:

  ```python
  device = Device.objects.get(id=device_id)
  ```

- **Добавление или обновление товара в корзине**:

  ```python
  basket_device, created = BasketDevice.objects.get_or_create(basket=basket, device=device)
  if not created:
      basket_device.quantity += quantity
      basket_device.save()
  else:
      basket_device.quantity = quantity
      basket_device.save()
  ```

  - **Если устройство уже в корзине — увеличиваем количество**.
  - **Если нет — добавляем новое**.

- **Ответ**:

  ```python
  return Response({'message': 'Device added to basket successfully.'}, status=status.HTTP_200_OK)
  ```

#### 📄 RemoveDeviceFromBasketView

```python
lookup_url_kwarg = 'basket_device_id'
```

- **Что это такое**:

  - **Указывает, что в URL запроса будет переменная `basket_device_id`**.
  - **Через неё мы будем искать какой конкретно товар удалять из корзины**.

- **Метод `delete`**:

  - **Получаем id товара из URL**:

    ```python
    basket_device_id = kwargs.get(self.lookup_url_kwarg)
    ```

  - **Находим корзину пользователя**:

    ```python
    basket = Basket.objects.filter(user=request.user).first()
    ```

  - **Находим нужный товар в корзине**:

    ```python
    basket_device = BasketDevice.objects.filter(id=basket_device_id, basket=basket).first()
    ```

  - **Если товара нет — `ошибка 404`**.

  - **Если товар найден — удаляем его**:

    ```python
    basket_device.delete()
    ```

  - **Отправляем сообщение об успешном удалении**.

## 7. Подключаем `вьюшки` через маршруты

```python
# baskets/urls.py

from django.urls import path
from .views import BasketDetailView, AddDeviceToBasketView, RemoveDeviceFromBasketView

urlpatterns = [
    # Получить свою корзину
    path('basket/', BasketDetailView.as_view(), name='basket-detail'),

    # Добавить устройство в корзину
    path('basket/add/', AddDeviceToBasketView.as_view(), name='basket-add-device'),

    # Удалить устройство из корзины (по id записи BasketDevice)
    path('basket/remove/<int:basket_device_id>/', RemoveDeviceFromBasketView.as_view(), name='basket-remove-device'),
]
```

### Объяснение:

```bash
/api/basket/	            GET	        Получить содержимое своей корзины
/api/basket/add/	        POST	    Добавить устройство в корзину
/api/basket/remove/<id>/	DELETE	    Удалить устройство из корзины
```

### Подключения этих маршрутов в общий проект

```python
# techstore_api/urls.py

from django.urls import path, include

urlpatterns = [
    # другие приложения...
    path('api/', include('baskets.urls')),
]
```

## 8. Описание `основных запросов` для `Basket` и `BasketDevice`

### Добавить устройство в корзину (`POST` `/api/basket/add/`)

#### Описание: Добавить товар в корзину.

- **Запрос**:
  - Метод: POST
  - URL: http://localhost:8000/api/basket/add/
- **Headers**:
  - Authorization: Bearer <твой токен>
  - Content-Type: application/json
- **Body (JSON)**:

  ```json
  {
    "device_id": 2
  }
  ```

  - Здесь device_id — это ID устройства (например, iPhone 15 имеет id = 2)

- **Ответ (успех)**:

  ```json
  {
    "message": "Device added to basket successfully."
  }
  ```

### Получить свою корзину (`GET` `/api/basket/`)

#### Описание: Получить содержимое корзины пользователя.

- **Запрос**:
  - Метод: GET
  - URL: http://localhost:8000/api/basket/
- **Headers**:
  - Authorization: Bearer <твой токен>
- **Ответ (пример)**:

  ```json
  {
    "id": 1,
    "user": 2,
    "devices": [
      {
        "id": 1,
        "title": "Galaxy S24",
        "description": "Флагман Samsung",
        "price": "899.99",
        "rating": 0.0,
        "type": 1,
        "brand": 2
      }
    ]
  }
  ```

### Удалить устройство из корзины (POST /api/basket/remove/)

#### Описание: Удалить товар из корзины.

- **Запрос**:
  - Метод: POST
  - URL: http://localhost:8000/api/basket/remove/
- **Headers**:
  - Authorization: Bearer <твой токен>
  - Content-Type: application/json
- **Body (JSON)**:

  ```json
  {
    "device_id": 2
  }
  ```

- **Ответ (успех)**:

  ```json
  {
    "message": "Device removed from basket successfully."
  }
  ```
