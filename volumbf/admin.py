from django.contrib import admin

from .models import Mentions, Stones, Typ 

class StonesAdmin(admin.ModelAdmin):
    list_display = ('title', 'legend', 'place', 'typ')
    list_display_links = ('title', 'legend', 'place')
    search_fields = ('title', 'legend', 'place'
                     #, 'work', 'author'
                     )

admin.site.register(Stones, StonesAdmin)
admin.site.register(Typ)
admin.site.register(Mentions)
