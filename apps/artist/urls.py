from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_create_artist),
    path('/<str:artist_id>', views.get_specific_artist),
    path('/<str:artist_id>/albums', views.get_create_artist_album),
    path('/<str:artist_id>/tracks', views.get_artist_tracks),
    path('/<str:artist_id>/albums/play', views.play_tracks),
]