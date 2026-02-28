from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from team.models import TeamMember


class TeamListView(ListView):
    model = TeamMember
    template_name = 'team/team.html'
    context_object_name = 'team'

class TeamDetailView(DetailView):
    model = TeamMember
    template_name = 'team/teamMemberDetail.html'
    context_object_name = 'teamMember'

class TeamEditView(UpdateView):
    model = TeamMember
    template_name = 'team/teamMemberEdit.html'
    context_object_name = 'teamMember'
    fields = '__all__'
    success_url = reverse_lazy('team:team')

class TeamDeleteView(DeleteView):
    model = TeamMember
    template_name = 'team/teamMemberDelete.html'
    context_object_name = 'teamMember'
    success_url = reverse_lazy('team:team')

class TeamCreateView(CreateView):
    model = TeamMember
    fields = '__all__'
    template_name = 'team/teamMemberCreate.html'
    success_url = reverse_lazy('team:team')
