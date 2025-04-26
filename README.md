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

# 3. Создание моделей приложения `devices`

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

- `ListCreateAPIView`:	Позволяет получить список всех объектов и создать новый. Автоматически обрабатывает методы GET и POST.
- `RetrieveUpdateDestroyAPIView`:	Позволяет получить объект по id, изменить его (PUT/PATCH) или удалить (DELETE).

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