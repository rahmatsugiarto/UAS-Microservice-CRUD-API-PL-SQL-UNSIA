from django.urls import path
from .views import UsersViewset


urlpatterns = [
    path('users/', UsersViewset.as_view()),
    path('users/<int:id>', UsersViewset.as_view())
]