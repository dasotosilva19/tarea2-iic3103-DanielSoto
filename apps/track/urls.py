from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_track),
    path('/<str:track_id>', views.get_specific_track),
    path('/<str:track_id>/play', views.play_track),
]