from django.db import models
from users.models import Users

# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class NoteLogger(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    message = models.TextField()