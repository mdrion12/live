from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # ------------------- JWT Token -------------------
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # ------------------- User Auth -------------------
    path('register/', views.RegisterAPI.as_view(), name='api-register'),
    path('login/', views.LoginAPI.as_view(), name='api-login'),
    path('logout/', views.LogoutAPI.as_view(), name='api-logout'),

    # ------------------- Match API -------------------
    path('api/matches/', views.match_list_create, name='match_list_create'),
    path('api/matches/<int:pk>/', views.match_detail, name='match_detail'),

    # ------------------- Over API -------------------
    path('api/over/', views.over_api, name='over_api'),

    # ------------------- Batting API -------------------
    path('api/batting/', views.batting_list_create, name='batting_list_create'),
    path('api/batting/<int:pk>/', views.batting_detail, name='batting_detail'),

    # ------------------- Extra API -------------------
    path('api/extra/', views.extra_singleton_api, name='extra_singleton_api'),

    # ------------------- Dashboard (Public) -------------------
    path('api/dashboard/', views.dashboard_view, name='dashboard_view'),
]
