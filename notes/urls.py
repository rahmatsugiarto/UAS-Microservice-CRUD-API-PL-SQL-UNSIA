from django.contrib import admin
from django.urls import path , include
from .views import NotesViewset

urlpatterns = [
    path('notes/', NotesViewset.as_view()),
]
