from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=30)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=300)
    token = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class UserLogger(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    message = models.TextField()