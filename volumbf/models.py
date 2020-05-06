from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from uuid import uuid4


def stones_directory_path_with_uuid(instance, filename):
    return '{}/{}'.format(instance.stones_id, uuid4())


class StonesManager(models.Manager):
    def all_with_prefetch_mentions(self):
        qs = self.get_queryset()
        return qs.prefetch_related('mentions')


class Stones(models.Model):
    title = models.CharField(max_length=30, verbose_name='Назва')
    place = models.TextField(verbose_name='Месцазнаходжанне')
    legend = models.TextField(null=True, blank=True, verbose_name='Легенда')
    typ = models.ForeignKey('Typ', null=True, on_delete=models.PROTECT, verbose_name='Тып')
    objects = StonesManager()
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

    def approved_comment(self):
        return self.comment.filter(approved_comment=True)


class Typ(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Назва тыпу')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Тыпы'
        verbose_name = 'Тып'
        ordering = ['name']


class StonesImage(models.Model):
    image = models.ImageField(upload_to=stones_directory_path_with_uuid)
    uploaded = models.DateTimeField(auto_now_add=True)
    stones = models.ForeignKey('Stones', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


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

class AuthorManager(models.Manager):
    def all_with_prefetch_movies_and_mentions(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed_by', 'publications__authors', 'role_set__movie'
        )

class Authors(models.Model):
    author = models.CharField(max_length=50, verbose_name='Аўтар')
    publications = models.ManyToManyField(Mentions, related_name='authors', verbose_name='Публікацыі', blank=True)
    objects = AuthorManager()

    def __str__(self):
        return self.author

    class Meta:
        verbose_name_plural = 'Аўтары'
        verbose_name = 'Аўтар'
        ordering = ['author']


class Comment(models.Model):
    stones = models.ForeignKey(Stones, on_delete=models.CASCADE, related_name='comment')
    commentator = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Каментары'
        verbose_name = 'Каментар'
        ordering = ['-created_date']


