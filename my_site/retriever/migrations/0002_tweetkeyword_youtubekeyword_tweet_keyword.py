# Generated by Django 4.1.7 on 2023-03-24 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retriever', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TweetKeyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeKeyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='keyword',
            field=models.ManyToManyField(to='retriever.tweetkeyword'),
        ),
    ]