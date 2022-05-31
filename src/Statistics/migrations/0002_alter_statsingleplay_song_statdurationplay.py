# Generated by Django 4.0.3 on 2022-05-31 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MusicApp', '0005_playlist_is_private_playlistfollow'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Statistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statsingleplay',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MusicApp.song'),
        ),
        migrations.CreateModel(
            name='StatDurationPlay',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now=True)),
                ('time_units', models.PositiveIntegerField()),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MusicApp.song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]