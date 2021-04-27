from django.db import models
from apps.artist.models import Artist

# Create your models here.


class Album(models.Model):
  ID = models.CharField(max_length=50, primary_key=True)
  name = models.CharField(max_length=100)
  genre = models.CharField(max_length=50)
  artists = models.URLField(max_length=200)
  tracks = models.URLField(max_length=200)
  self_url = models.URLField(max_length=200)
  artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
