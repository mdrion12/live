from django.urls import path
from . import views

urlpatterns = [
    path('api/matches/', views.match_list_create, name='match_list_create'),
    path('api/matches/<int:pk>/', views.match_detail, name='match_detail'),
    path('api/over/', views.over_api, name='over_api'),
    path('api/batting/',views.batting_list_create, name='batting_list_create'),
    path('api/batting/<int:pk>/', views.batting_detail, name='batting_detail'),
    path('api/extra/', views.extra_singleton_api, name='extra_singleton_api'),
    path('batting/total_score/', views.total_score, name='total_score'),
    path('create-superuser/', views.create_superuser),
]
