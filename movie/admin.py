from django.contrib import admin

from movie.models import Movie, Role

admin.site.register(Movie)
admin.site.register(Role)