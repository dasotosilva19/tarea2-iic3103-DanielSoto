from django.shortcuts import render
from django.http import JsonResponse
from . import models
from apps.track.models import Track
from django.views.decorators.csrf import csrf_exempt
import json
from base64 import b64encode


# Create your views here.
def get_album(request):
  if request.method == 'GET':

    albums = models.Album.objects.all()
    
    albums_array = [{'id': album.ID, 'artist_id': album.artist_id.ID, 'name': album.name, 
    'genre': album.genre, 'artist': album.artists, 'tracks': album.tracks,
    'self': album.self_url} for album in albums]

    return JsonResponse(albums_array, status=200, safe=False)


def get_specific_album(request, album_id):
  if request.method == 'GET':
    exist = models.Album.objects.filter(ID=album_id)

    if len(exist) != 0:
      return JsonResponse({"id": exist[0].ID, "artist_id": exist[0].artist_id.ID, "name": exist[0].name, 
      "genre": exist[0].genre, "artist": exist[0].artists, "tracks": exist[0].tracks,
      "self": exist[0].self_url}, status=200)

    else:
      return JsonResponse({'msg': 'álbum no encontrado'}, status=404)

@csrf_exempt
def get_create_specific_album_tracks(request, album_id):
  if request.method == 'GET':
    exist = models.Album.objects.filter(ID=album_id)

    if len(exist) != 0:
      tracks = Track.objects.filter(album_id=album_id)

      tracks_array = [{'id': track.ID, 'album_id': track.album_id.ID, 'name': track.name, 
      'duration': track.duration, 'times_played': track.times_played, 'artist': track.artists,
      'album': track.albums, 'self': track.self_url} for track in tracks]

      return JsonResponse(tracks_array, status=200, safe=False)

    else:
      return JsonResponse({'msg': 'álbum no encontrado'}, status=404)
  
  elif request.method == 'POST':
    params = json.loads(request.body)

    if (not "name" in params.keys()) or (not "duration" in params.keys()):
      return JsonResponse({"msg": "input inválido"}, status=400)

    if (type(params["name"]) != str) or (type(params["duration"]) != float):
      return JsonResponse({"msg": "input inválido"}, status=400)


    name = params['name']+":"+album_id
    ID_encoded = b64encode(name.encode()).decode('utf-8')[0:22]
    print(ID_encoded)
    album_exist = models.Album.objects.filter(ID=album_id)

    if len(album_exist) == 0:
      return JsonResponse({'msg': 'álbum no existe'}, status=422)

    else:
      exist = Track.objects.filter(ID=ID_encoded)

      if len(exist) == 0:

        url_artists = "/artists/{}".format(album_exist[0].artist_id.ID)
        url_albums = "/albums/{}".format(album_id)
        url_self_tracks = "/tracks/{}".format(ID_encoded)

        new_track = Track.objects.create(ID=ID_encoded,
        name=params["name"], duration=params["duration"], times_played=0, 
        albums=url_albums, artists=url_artists, self_url=url_self_tracks, album_id=album_exist[0])

        new_track.save()

        return JsonResponse({"id": ID_encoded, "album_id": album_id, 
        "name": params["name"], "duration": params["duration"], "times_played": 0,
        "artist": url_artists, "album": url_albums, "self": url_self_tracks}, status=201)

      else:
        return JsonResponse({"id": exist[0].ID, "album_id": exist[0].album_id.ID, "name": exist[0].name, 
        "duration": exist[0].duration, "times_played": exist[0].times_played,
        "artist": exist[0].artists, "album": exist[0].albums, "self": exist[0].self_url}, status=409)

@csrf_exempt
def play_tracks(request, album_id):
  if request.method == 'PUT':
    album = models.Album.objects.filter(ID = album_id)

    if len(album) != 0:
      tracks = Track.objects.filter(album_id=album[0])

      for track in tracks:
        track.times_played += 1
        track.save()
      
      return JsonResponse({"msg": "canciones del álbum reproducidas"}, status=200)

    else:
      return JsonResponse({"msg": "álbum no encontrado"}, status=404)