# Generated by Django 4.2 on 2023-07-27 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorin', '0005_alter_post_image_alter_post_publication_date_post_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pfp',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]