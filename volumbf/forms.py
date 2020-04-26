from django.forms import ModelForm

from .models import Stones, Mentions, Authors, Comment


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