from rest_framework import generics
from .models import User
from .serializers import UserSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

class UserRegisterView(generics.CreateAPIView):
    """
    Представление для регистрации пользователей

    Доступно для всех без авторизации
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveAPIView):
    """
    Представление для получения данных текущего пользователя
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer