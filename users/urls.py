from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginAPI.as_view(), name='user_login'),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('logout/', TokenBlacklistView.as_view(), name='user_logout'),

]
