from django.db import models

# Create your models here.
class AuthenticationLogger(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    message = models.TextField()