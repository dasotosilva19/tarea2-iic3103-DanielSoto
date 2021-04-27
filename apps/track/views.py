from django.shortcuts import render
from django.http import JsonResponse
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
from base64 import b64encode

# Create your views here.


def get_track(request):
  if request.method == 'GET':
    tracks = models.Track.objects.all()
    
    tracks_array = [{'id': track.ID, 'album_id': track.album_id.ID, 'name': track.name, 
    'duration': track.duration, 'times_played': track.times_played, 'artist': track.artists,
    'album': track.albums, 'self': track.self_url} for track in tracks]

    return JsonResponse(tracks_array, status=200, safe=False)

def get_specific_track(request, track_id):
  if request.method == 'GET':
    exist = models.Track.objects.filter(ID=track_id)

    if len(exist) != 0:
      return JsonResponse({'id': exist[0].ID, 'album_id': exist[0].album_id.ID, 'name': exist[0].name, 
    'duration': exist[0].duration, 'times_played': exist[0].times_played, 'artist': exist[0].artists,
    'album': exist[0].albums, 'self': exist[0].self_url}, status=200)
    
    else:
      return JsonResponse({'msg': 'Canción no encontrada'}, status=404)
