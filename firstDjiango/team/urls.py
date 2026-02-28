from django.urls import path
from team.views import TeamListView, TeamDetailView, TeamEditView, TeamDeleteView, TeamCreateView

app_name = 'team'

urlpatterns = [
    path('all/', TeamListView.as_view(), name='team'),
    path('create/', TeamCreateView.as_view(), name='team_create'),
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
    path('team/<int:pk>/update/',TeamEditView.as_view(), name='team_update'),
    path('team/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),
]
