from django import forms
from django.contrib.auth.models import User

from .models import Album, Sarki


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['sarkici', 'album_basligi', 'tur', 'album_logo']


class SarkiForm(forms.ModelForm):
    class Meta:
        model=Sarki
        fields=['sarki_basligi','ses_dosyalari']


class UserForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username','email','password']
