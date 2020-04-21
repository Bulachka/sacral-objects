from django.db import models
from django.core.exceptions import ValidationError

class Stones(models.Model):
    title = models.CharField(max_length=30, verbose_name='Назва')
    place = models.TextField(verbose_name='Месцазнаходжанне')
    legend = models.TextField(null=True, blank=True, verbose_name='Легенда')
    typ = models.ForeignKey('Typ', null=True, on_delete=models.PROTECT, verbose_name='Тып')
    def __str__(self):
        return self.title

    def clean(self):
        errors = {}
        if not self.legend:
            errors['legend'] = ValidationError('Дадайце легенду')
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name_plural = 'Камяні'
        verbose_name = 'Камень'
        #ordering = ['title']
        order_with_respect_to = 'typ'
        unique_together = ('title', 'place')

class Typ(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Назва тыпу')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Тыпы'
        verbose_name = 'Тып'
        ordering = ['name']


class Mentions(models.Model):
    work = models.TextField(verbose_name='Праца')
    year = models.PositiveIntegerField(blank=True, null=True)
    sacral_objects = models.ManyToManyField(Stones, related_name='mentions', verbose_name='Сакральны аб\'ект')
    def __str__(self):
        return self.work

    class Meta:
        verbose_name_plural = 'Узгадкі'
        verbose_name = 'Узгадка'
        ordering = ['work']


class Authors(models.Model):
    author = models.CharField(max_length=50, verbose_name='Аўтар')
    publications = models.ManyToManyField(Mentions, related_name='authors', verbose_name='Аўтары')
    def __str__(self):
        return self.author

    class Meta:
        verbose_name_plural = 'Аўтары'
        verbose_name = 'Аўтар'
        ordering = ['author']

