from django.db import models
from volumbf.models import Authors, Stones, Mentions

class MovieManager(models.Manager):
    def all_with_related_authors(self):
        qs = self.get_queryset()
        qs = qs.prefetch_related('director', 'creators')
        return qs

class Movie(models.Model):
    DOCUMENTARY = 0
    ART = 1
    NEWSREEL = 2
    REPORTAGE = 3
    RATINGS = (
        (DOCUMENTARY, 'Знята ў час аўтэнтычнага абрада'),
        (ART, 'Мастацкае асэнсаванне'),
        (NEWSREEL, 'Апрацаваны запіс аўтэнтычнага абраду'),
        (REPORTAGE, 'Непасрэдная перадача падзеі'),
    )

    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(
        choices=RATINGS,
        default=DOCUMENTARY)
    director = models.ManyToManyField(to='volumbf.Authors', related_name='directed_by', blank=True)
    creators = models.ManyToManyField(to='volumbf.Authors', through='Role', related_name='created_by', blank=True)
    website = models.URLField(blank=True)
    objects = MovieManager()

    class Meta:
        ordering = ('-year', 'title')
        verbose_name = 'Фільм'
        verbose_name_plural = 'Фільмы'

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)
    
class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING, verbose_name='Фільм')
    author = models.ForeignKey(Authors, on_delete=models.DO_NOTHING, verbose_name='Аўтар')
    participation = models.CharField(max_length=140)

    def __str__(self):
        return "{} {} {}".format(self.movie.title, self.author.author, self.participation)

    class Meta:
        unique_together = ('movie', 'author', 'participation')
        verbose_name = 'Удзел'
        verbose_name_plural = 'Удзел'

