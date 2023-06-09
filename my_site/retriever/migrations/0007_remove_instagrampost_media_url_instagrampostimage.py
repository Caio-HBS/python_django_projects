# Generated by Django 4.1.7 on 2023-04-03 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('retriever', '0006_alter_instagrampost_media_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagrampost',
            name='media_url',
        ),
        migrations.CreateModel(
            name='InstagramPostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=300)),
                ('instagram_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retriever.instagrampost')),
            ],
        ),
    ]
