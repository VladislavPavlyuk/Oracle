from django.views.generic import ListView
from team.models import TeamMember


class TeamListView(ListView):
    model = TeamMember
    template_name = 'team/team.html'
    context_object_name = 'team'
