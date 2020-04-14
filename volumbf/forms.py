from django.forms import ModelForm

from .models import Stones

class StonesForm(ModelForm):
    class Meta:
        model = Stones
        fields = ('title', 'legend', 'place', 'typ')
