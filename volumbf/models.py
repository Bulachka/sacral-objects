from django.db import models

def run_shell(use_plain=False):
    from django.db.models.loading import get_models
    loaded_models = get_models()

class Stones(models.Model):
    title = models.CharField(max_length=30, verbose_name='Назва')
    place = models.TextField(verbose_name='Месцазнаходжанне')
    legend = models.TextField(null=True, blank=True, verbose_name='Легенда')
    typ = models.ForeignKey('Typ', null=True, on_delete=models.PROTECT, verbose_name='Тып')
    def __str__(self):
        return self.title

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
    author = models.CharField(max_length=50, verbose_name='Аўтар')
    work = models.TextField(verbose_name='Праца')
    sacral_objects = models.ManyToManyField(Stones, verbose_name='Сакральны аб\'ект')
    def __str__(self):
        return self.work

    class Meta:
        verbose_name_plural = 'Узгадкі'
        verbose_name = 'Узгадка'
        ordering = ['author']
        unique_together = ('author', 'work')


