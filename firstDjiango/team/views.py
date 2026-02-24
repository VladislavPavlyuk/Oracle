from django.shortcuts import render
from team.models import Worker

# Create your views here.
def team(request):
    context = {
        'workers': Worker.objects.all()
    }
    return render(request, 'team/team.html', context)
