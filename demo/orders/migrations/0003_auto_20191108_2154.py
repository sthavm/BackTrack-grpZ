# Generated by Django 2.2.6 on 2019-11-08 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20191108_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devteammember',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.Project'),
        ),
        migrations.AlterField(
            model_name='productowner',
            name='project',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.Project'),
        ),
    ]
