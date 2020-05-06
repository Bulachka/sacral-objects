from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms
from .models import Stones, Mentions, Authors, Comment, StonesImage


class StonesForm(ModelForm):
    class Meta:
        model = Stones
        fields = ('title', 'legend', 'place', 'typ')


class MentionsForm(ModelForm):
    class Meta:
        model = Mentions
        fields = ('work', 'year', 'sacral_objects')


class AuthorsForm(ModelForm):
    class Meta:
        model = Authors
        fields = ('author', 'publications')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('commentator', 'text')


class StonesImageForm(ModelForm):
    stones = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Stones.objects.all(),
        disabled=True
    )
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True
    )
    class Meta:
        model = StonesImage
        fields = ('image', 'user', 'stones')