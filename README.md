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

# 3. Добавление логина с использованием `JWT`

## 1. Установить библиотеку Simple JWT

```bash
pip install djangorestframework-simplejwt
```

## 2. Настроить аутентификацию в settings.py

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

## 3. Добавить URL-маршруты для логина/обновления токена (users/urls.py)

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

## 4. (Необязательно) Кастомизация ответа при логине (дополнительно)

Можно дополнить стандартный логин-эндпоинт своим выводом. Например, чтобы возвращать ещё и роль пользователя.

### Создадим свой сериализатор:

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

### своё представление:

```python
# users/views.py

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```

### в users/urls.py нужно поменять импорт:

```python
from .views import UserRegisterView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),  # Наш кастомный логин
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
```

Теперь токен будет содержать ещё `username` и `role` — это удобно на фронте для быстрого понимания, кто вошёл.

## 5. Как пользоваться

### Для регистрации: POST /api/users/register/

**тело запроса**:

```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "secret123",
  "role": "customer"
}
```

### Для логина: POST /api/users/login/

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

### Для обновления токена: POST /api/users/refresh/

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

# 4. Получение профиля текущего пользователя `/me/

## 1. Добавить сериализатор для просмотра профиля

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

## 2. Добавить вьюшку для получения данных текущего пользователя

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

## 3. Добавить эндпоинт в users/urls.py

```python
from .views import UserRegisterView, CustomTokenObtainPairView, UserProfileView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
]
```

## 4. Как пользоваться `/me/`

### Запрос: `GET /api/users/me/`

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
