from django.contrib import admin

from .models import Stones
from .models import Typ

class StonesAdmin(admin.ModelAdmin):
    list_display = ('title', 'legend', 'place', 'typ')
    list_display_links = ('title', 'legend', 'place')
    search_fields = ('title', 'legend', 'place')

admin.site.register(Stones, StonesAdmin)
admin.site.register(Typ)
