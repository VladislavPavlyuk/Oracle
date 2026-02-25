from django.views.generic import ListView
from team.models import teamMember


class TeamListView(ListView):
    model = teamMember
    template_name = 'team/team.html'
    context_object_name = 'team'


# Create your views here.
# def team(request):
#    context = {
#        'workers': teamMember.objects.all()
#    }
#    return render(request, 'team/team.html', context)
