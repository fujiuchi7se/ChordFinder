from django.db import models

class ChordProgression(models.Model):
    song_title = models.CharField(max_length=200)
    singer = models.CharField(max_length=200)
    key = models.CharField(max_length=10)
    progression = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.song_title