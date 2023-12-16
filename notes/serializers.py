from rest_framework import serializers
from .models import Note
from users.serializers import UsersSerializer

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        ordering = ['id']
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']