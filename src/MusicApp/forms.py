from django import forms


class PlaylistForm(forms.Form):
    name = forms.CharField(max_length=255)