from django.urls import path
from team.views import team

urlpatterns = [
    path('all/', team, name='team'),
]