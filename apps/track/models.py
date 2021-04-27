from django.db import models
from apps.album.models import Album

# Create your models here.


class Track(models.Model):
  ID = models.CharField(max_length=50, primary_key=True)
  name = models.CharField(max_length=100)
  duration = models.FloatField()
  times_played = models.IntegerField()
  albums = models.URLField(max_length=200)
  artists = models.URLField(max_length=200)
  self_url = models.URLField(max_length=200)
  album_id = models.ForeignKey(Album, on_delete=models.CASCADE)