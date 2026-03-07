from team.models import TeamMember


def team_count(request):
    context = {
        'team_count': TeamMember.objects.count()
    }
    return context
