from django.urls import path
from team.views import TeamListView

urlpatterns = [
    path('all/', TeamListView.as_view(), name='team'),
]
