from django.db import models
from django.core.urlresolvers import reverse
class Album(models.Model):

    artist=models.CharField(max_length=250)
    album_title=models.CharField(max_length=250)
    genre=models.CharField(max_length=250)
    album_logo=models.CharField(max_length=250)

    def get_absolute_url(self):
        return reverse('music/detail',kwargs={'pk':self.pk})
    def __str__(self):
        return self.album_title + " " + self.artist

class Song(models.Model):

    def __str__(self):
        return self.song_name

    album=models.ForeignKey(Album,on_delete=models.CASCADE)
    file_type=models.CharField(max_length=20)
    song_name=models.CharField(max_length=250)
    is_favourite=models.BooleanField(default=False)


