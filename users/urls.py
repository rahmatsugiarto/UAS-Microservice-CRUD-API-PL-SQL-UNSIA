from django.urls import path
from .views import UsersByPassViewset, UsersViewset


urlpatterns = [
    path('users/', UsersViewset.as_view()),
    path('usersByPass/', UsersByPassViewset.as_view()),
]