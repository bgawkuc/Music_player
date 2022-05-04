from django.contrib.auth.models import User
from django.db import models

from MusicApp.models import Song


class StatSinglePlay(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    song = models.ForeignKey(Song, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now=True)
    count = models.PositiveIntegerField(default=0)

    def increaseCount(self):
        self.count += 1
