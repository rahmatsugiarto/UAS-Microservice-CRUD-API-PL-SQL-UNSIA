# Generated by Django 5.0 on 2023-12-12 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='token',
            field=models.TextField(blank=True, null=True),
        ),
    ]