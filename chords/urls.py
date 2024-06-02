from django.urls import path
from . import views

urlpatterns = [
    path('', views.key_list, name='key_list'),
    path('key/<str:key>/', views.song_list, name='song_list'),
    path('song/<int:song_id>/', views.song_detail, name='song_detail'),
]