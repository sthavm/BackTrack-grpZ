# Generated by Django 2.2.6 on 2019-11-25 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('title', 'pbi')},
        ),
    ]
