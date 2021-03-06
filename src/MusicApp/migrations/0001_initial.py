# Generated by Django 4.0.3 on 2022-04-07 00:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SongDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bpm', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('energy', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('danceability', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('loudness', models.IntegerField(validators=[django.core.validators.MaxValueValidator(0)])),
                ('liveness', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('valence', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('acousticness', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('speechiness', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('artist', models.CharField(max_length=50)),
                ('song_link', models.CharField(max_length=255)),
                ('image_link', models.CharField(max_length=255)),
                ('length', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MusicApp.songdetail')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MusicApp.genre')),
            ],
        ),
    ]
