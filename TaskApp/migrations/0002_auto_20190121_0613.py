# Generated by Django 2.1.5 on 2019-01-21 06:13

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TaskApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='creator',
        ),
        migrations.AddField(
            model_name='task',
            name='creator',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.CharField(max_length=20, verbose_name=django.contrib.auth.models.User),
        ),
    ]