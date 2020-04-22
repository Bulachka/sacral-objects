from django.db import models

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
    director = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)
    


