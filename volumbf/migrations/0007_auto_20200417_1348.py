# Generated by Django 3.0.4 on 2020-04-17 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volumbf', '0006_merge_20200417_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentions',
            name='sacral_objects',
            field=models.ManyToManyField(related_name='stones', to='volumbf.Stones', verbose_name="Сакральны аб'ект"),
        ),
    ]
