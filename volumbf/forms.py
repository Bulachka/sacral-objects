from django.forms import ModelForm

from .models import Stones, Mentions, Authors

class StonesForm(ModelForm):
    class Meta:
        model = Stones
        fields = ('title', 'legend', 'place', 'typ')

class MentionsForm(ModelForm):
    class Meta:
        model = Mentions
        fields = ('work', 'year')

class AuthorsForm(ModelForm):
    class Meta:
        model = Authors
        fields = ('author', )
