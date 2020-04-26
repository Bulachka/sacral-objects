from django.urls import path
from . import views
from .views import movie_new, movie_edit

app_name = 'movie'
urlpatterns = [
    path('movies/', views.MovieList.as_view(), name='MovieList'),
    path('movie/<int:pk>/', views.MovieDetail.as_view(), name='MovieDetail'),
    path('movie/new/', movie_new, name='movie_new'),
    path('movie/<int:pk>/edit/', movie_edit, name='movie_new'),

]
