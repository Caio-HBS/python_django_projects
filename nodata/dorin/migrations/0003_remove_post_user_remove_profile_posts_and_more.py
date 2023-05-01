# Generated by Django 4.2 on 2023-04-28 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dorin', '0002_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='posts',
        ),
        migrations.AddField(
            model_name='post',
            name='parent_profile',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dorin.profile'),
            preserve_default=False,
        ),
    ]
