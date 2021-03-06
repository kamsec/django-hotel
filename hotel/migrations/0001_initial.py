# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-09-15 14:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=30)),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('category', models.PositiveSmallIntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='rooms',
            field=models.ManyToManyField(to='hotel.Room'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
