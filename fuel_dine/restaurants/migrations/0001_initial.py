# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='text')),
                ('posted_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='posted_at')),
            ],
            options={
                'ordering': ['-posted_at'],
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_score', models.IntegerField(db_index=True, default=0)),
                ('num_vote_up', models.PositiveIntegerField(db_index=True, default=0)),
                ('num_vote_down', models.PositiveIntegerField(db_index=True, default=0)),
                ('lat', models.FloatField(verbose_name='latitude')),
                ('lon', models.FloatField(verbose_name='longitude')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('website', models.URLField(blank=True, null=True, verbose_name='website')),
                ('address', models.TextField(help_text='Location of the restaurant', verbose_name='Address')),
                ('contact', models.CharField(blank=True, max_length=10, null=True, verbose_name='contact')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at')),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'restaurant',
                'verbose_name_plural': 'restaurants',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='text')),
                ('posted_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='posted_at')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.Restaurant', verbose_name='restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile', verbose_name='user')),
            ],
            options={
                'ordering': ['-posted_at'],
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.Restaurant', verbose_name='restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile', verbose_name='user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.Review', verbose_name='review'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile', verbose_name='user'),
        ),
    ]
