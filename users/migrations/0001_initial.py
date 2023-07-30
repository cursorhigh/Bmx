# Generated by Django 4.2.3 on 2023-07-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('rank', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('score', models.IntegerField(default=0)),
                ('wins', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['rank'],
            },
        ),
    ]
