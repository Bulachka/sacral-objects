from django.shortcuts import render
from django.views.generic import (ListView, DetailView,)

from movie.models import Movie

class MovieList(ListView):
    model = Movie

class MovieDetail(DetailView):
    queryset = (Movie.objects.all_with_related_authors())