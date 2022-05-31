from django import forms


class PlaylistForm(forms.Form):
    name = forms.CharField(max_length=255)
    is_private = forms.BooleanField(required=False)  # initial for unchecked checkbox


class SearchQueryForm(forms.Form):
    query = forms.CharField()
