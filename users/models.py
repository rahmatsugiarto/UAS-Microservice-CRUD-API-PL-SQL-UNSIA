from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=30)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=300)
    token = models.TextField(null=True, blank=True)