from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_album),
    path('/<str:album_id>', views.get_specific_album),
    path('/<str:album_id>/tracks', views.get_create_specific_album_tracks),
]