from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import UserRegisterView, UserProfileView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', UserProfileView.as_view(), name='user-profile')
]
