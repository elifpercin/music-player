from django.contrib.auth.models import User #kimlik doğrulama modellerını içerir
from django.db import models


class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    sarkici = models.CharField(max_length=250)
    album_basligi = models.CharField(max_length=250)
    tur = models.CharField(max_length=250)
    album_logo = models.FileField()
    favoriler = models.BooleanField(default=False)

    def __str__(self):
        return self.album_basligi + ' - ' + self.sarkici


class Sarki(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    sarki_basligi =models.CharField(max_length=250)
    ses_dosyalari=models.FileField(default='')
    favoriler=models.BooleanField(default=False)

    def __str__(self):
        return self.sarki_basligi
