from django import forms


class PlaylistForm(forms.Form):
    name = forms.CharField(max_length=255)

class SearchQueryForm(forms.Form):
    query = forms.CharField()
