# Generated by Django 3.0.4 on 2020-04-26 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volumbf', '0014_auto_20200426_1302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='stone',
            new_name='stones',
        ),
    ]
