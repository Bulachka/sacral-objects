from django import forms
# from django.contrib.auth import get_user_model

from .models import Movie


class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = ('title', 'plot', 'year', 'rating', 'director', 'creators', 'website')


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    to_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

"""
class VoteForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True,
    )
    movie = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Movie.objects.all(),
        disabled=True,
    )
    value = forms.ModelChoiceField(
        label="Vote",
        widget=forms.RadioSelect,
        choices=Vote.VALUE_CHOICES,
    )

    class Meta:
        model = Vote
        fields = ('value', 'user', 'movie')

"""