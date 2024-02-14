# Generated by Django 5.0 on 2024-02-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_users_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLogger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('method', models.CharField(max_length=10)),
                ('message', models.TextField()),
            ],
        ),
    ]
