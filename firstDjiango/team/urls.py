from django.urls import path

from team.views import (
    TeamCreateView,
    TeamContactCreateView,
    TeamContactDeleteView,
    TeamContactDetailView,
    TeamContactUpdateView,
    TeamDeleteView,
    TeamDetailView,
    TeamEditView,
    TeamGenerateDataView,
    TeamListView,
    TeamResumeCreateView,
    TeamResumeDeleteView,
    TeamResumeDetailView,
    TeamResumeListView,
    TeamResumeUpdateView, TeamSearchView,
)

app_name = "team"

urlpatterns = [
    path("all/", TeamListView.as_view(), name="team"),
    path("generate-data/", TeamGenerateDataView.as_view(), name="generate_data"),
    path("create/", TeamCreateView.as_view(), name="team_create"),
    path("team/<int:pk>/", TeamDetailView.as_view(), name="team_detail"),
    path("team/<int:pk>/update/", TeamEditView.as_view(), name="team_update"),
    path("team/<int:pk>/delete/", TeamDeleteView.as_view(), name="team_delete"),
    path("resumes/", TeamResumeListView.as_view(), name="resume_list"),
    path("team/<int:member_pk>/resume/", TeamResumeDetailView.as_view(), name="resume_detail"),
    path("team/<int:member_pk>/resume/create/", TeamResumeCreateView.as_view(), name="resume_create"),
    path("team/<int:member_pk>/resume/update/", TeamResumeUpdateView.as_view(), name="resume_update"),
    path("team/<int:member_pk>/resume/delete/", TeamResumeDeleteView.as_view(), name="resume_delete"),
    path("team/<int:member_pk>/contacts/create/", TeamContactCreateView.as_view(), name="contact_create"),
    path("team/<int:member_pk>/contacts/<int:contact_pk>/", TeamContactDetailView.as_view(), name="contact_detail"),
    path("team/<int:member_pk>/contacts/<int:contact_pk>/update/", TeamContactUpdateView.as_view(), name="contact_update"),
    path("team/<int:member_pk>/contacts/<int:contact_pk>/delete/", TeamContactDeleteView.as_view(), name="contact_delete"),
    path('search/', TeamSearchView.as_view(), name='team_search'),
]
