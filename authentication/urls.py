from django.urls import path
from .views import AuthViewset


urlpatterns = [
    path('login/', AuthViewset.as_view()),
]