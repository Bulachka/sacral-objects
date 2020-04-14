from django.db import models

class Stones(models.Model):
    title = models.CharField(max_length=30, verbose_name='Назва')
    place = models.TextField(verbose_name='Месцазнаходжанне')
    legend = models.TextField(null=True, blank=True, verbose_name='Легенда')
    typ = models.ForeignKey('Typ', null=True, on_delete=models.PROTECT, verbose_name='Тып')

    class Meta:
        verbose_name_plural = 'Камяні'
        verbose_name = 'Камень'
        ordering = ['title']
        #order_with_respect_to = 'typ'
        unique_together = ('title', 'place')

class Typ(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Назва тыпу')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Тыпы'
        verbose_name = 'Тып'
        ordering = ['name']
'''

class Mentions(models.Model):
    author = models.CharField(max_length=50, verbose_name='Аўтар')
    work = models.TextField(verbose_name='Праца')
    year = models.DateField(null=True, blank=True, verbose_name='Дата ўзгадкі')
    sacral_objects = models.ManyToManyField(Stones, null=True, on_delete=models.PROTECT, verbose_name='Сакральны аб\'ект')

    class Meta:
        verbose_name_plural = 'Узгадкі'
        verbose_name = 'Узгадка'
        ordering = ['author']
        unique_together = ('author', 'work')

'''
