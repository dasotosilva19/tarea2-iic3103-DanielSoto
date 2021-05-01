from django.shortcuts import render
from django.http import JsonResponse
from . import models
from apps.album.models import Album
from apps.track.models import Track
from django.views.decorators.csrf import csrf_exempt
import json
from base64 import b64encode

# Create your views here.
@csrf_exempt
def get_create_artist(request):
  if request.method == 'GET':

    artists = models.Artist.objects.all()
    
    artists_array = [{'id': artist.ID, 'name': artist.name, 
    'age': artist.age, 'albums': artist.albums, 'tracks': artist.tracks,
    'self': artist.self_url} for artist in artists]

    return JsonResponse(artists_array, status=200, safe=False)

  elif request.method == 'POST':

    params = json.loads(request.body)

    if (not "name" in params.keys()) or (not "age" in params.keys()):
      return JsonResponse({}, status=400)

    if (type(params["name"]) != str) or (type(params["age"]) != int):
       return JsonResponse({}, status=400)

    name = params['name']
    age = params['age']
    ID_encoded = b64encode(name.encode()).decode('utf-8')

    exist = models.Artist.objects.filter(ID=ID_encoded)
    if len(exist) == 0:

      url_albums = "https://{}/artists/{}/albums".format(request.get_host(), ID_encoded)
      url_tracks = "https://{}/artists/{}/tracks".format(request.get_host(), ID_encoded)
      url_self_artist = "https://{}/artists/{}".format(request.get_host(), ID_encoded)

      new_artist = models.Artist.objects.create(ID=ID_encoded,
      name=name, age=age, albums=url_albums, tracks=url_tracks,
      self_url=url_self_artist)

      new_artist.save()

      return JsonResponse({"id": ID_encoded, "name": name, "age": age, 
      "albums": url_albums, "tracks": url_tracks, "self": url_self_artist}, status=201)

    else:
      return JsonResponse({"id": exist[0].ID, "name": exist[0].name, 
      "age": exist[0].age, "albums": exist[0].albums, "tracks": exist[0].tracks,
      "self": exist[0].self_url}, status=409)

  else:
    return JsonResponse({}, status=405)


@csrf_exempt
def get_specific_artist(request, artist_id):
  if request.method == 'GET':
    exist = models.Artist.objects.filter(ID=artist_id)

    if len(exist) != 0:
      return JsonResponse({"id": exist[0].ID, "name": exist[0].name, 
      "age": exist[0].age, "albums": exist[0].albums, "tracks": exist[0].tracks,
      "self": exist[0].self_url}, status=200)

    else:
      return JsonResponse({}, status=404)

  elif request.method == 'DELETE':
    exist = models.Artist.objects.filter(ID=artist_id)

    if len(exist) != 0:
      exist[0].delete()

      return JsonResponse({}, status=204)

    else:
      return JsonResponse({}, status=404)

  else:
    return JsonResponse({}, status=405)

@csrf_exempt
def get_create_artist_album(request, artist_id):
    if request.method == 'GET':
      exist = models.Artist.objects.filter(ID=artist_id)

      if len(exist) != 0:
        albums = Album.objects.filter(artist_id=artist_id)

        albums_array = [{'id': album.ID, 'artist_id': album.artist_id.ID, 'name': album.name, 
        'genre': album.genre, 'artist': album.artists, 'tracks': album.tracks,
        'self': album.self_url} for album in albums]

        return JsonResponse(albums_array, status=200, safe=False)

      else:
        return JsonResponse({}, status=404)

    elif request.method == 'POST':
      params = json.loads(request.body)

      if (not "name" in params.keys()) or (not "genre" in params.keys()):
        return JsonResponse({}, status=400)

      if (type(params["name"]) != str) or (type(params["genre"]) != str):
        return JsonResponse({}, status=400)


      name = params['name']+":"+artist_id
      ID_encoded = b64encode(name.encode()).decode('utf-8')[0:22]

      artist_exist = models.Artist.objects.filter(ID=artist_id)

      if len(artist_exist) == 0:
        return JsonResponse({}, status=422)

      else:
        exist = Album.objects.filter(ID=ID_encoded)

        if len(exist) == 0:

          url_artists = "https://{}/artists/{}".format(request.get_host(), artist_id)
          url_tracks = "https://{}/albums/{}/tracks".format(request.get_host(), ID_encoded)
          url_self_album = "https://{}/albums/{}".format(request.get_host(), ID_encoded)

          new_artist = Album.objects.create(ID=ID_encoded,
          name=params["name"], genre=params["genre"], artists=url_artists, tracks=url_tracks,
          self_url=url_self_album, artist_id=artist_exist[0])

          new_artist.save()

          return JsonResponse({"id": ID_encoded, "artist_id": artist_id, 
          "name": params["name"], "genre": params["genre"], "artist": url_artists, 
          "tracks": url_tracks, "self": url_self_album}, status=201)

        else:
          return JsonResponse({"id": exist[0].ID, "artist_id": exist[0].artist_id.ID, "name": exist[0].name, 
          "genre": exist[0].genre, "artist": exist[0].artists, "tracks": exist[0].tracks,
          "self": exist[0].self_url}, status=409)

    else:
      return JsonResponse({}, status=405)

@csrf_exempt
def get_artist_tracks(request, artist_id):
  if request.method == 'GET':
    exist = models.Artist.objects.filter(ID=artist_id)

    if len(exist) != 0:
      albums = Album.objects.filter(artist_id=artist_id)
      tracks = []

      for album in albums:
        album_tracks = Track.objects.filter(album_id=album.ID)

        for album_track in album_tracks:
          tracks.append(album_track)

      tracks_array = [{'id': track.ID, 'album_id': track.album_id.ID, 'name': track.name, 
      'duration': track.duration, 'times_played': track.times_played, 'artist': track.artists,
      'album': track.albums, 'self': track.self_url} for track in tracks]

      return JsonResponse(tracks_array, status=200, safe=False)

    else:
      return JsonResponse({}, status=404)

  else:
    return JsonResponse({}, status=405)

@csrf_exempt
def play_tracks(request, artist_id):
  if request.method == 'PUT':
    artist = models.Artist.objects.filter(ID=artist_id)

    if len(artist) != 0:
      albums = Album.objects.filter(artist_id = artist_id)

      for album in albums:
        tracks = Track.objects.filter(album_id=album.ID)

        for track in tracks:
          track.times_played += 1
          track.save()

      return JsonResponse({}, status=200)

    else:
      return JsonResponse({}, status=404)

  else:
    return JsonResponse({}, status=405)