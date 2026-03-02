from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from team.models import Contact, Resume, TeamMember
from team.fabric import TeamDataFabric


class MessageOnFormMixin:
    success_message = None
    error_message = "Please correct the form errors and try again."

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        if self.error_message:
            messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class MessageOnDeleteMixin:
    delete_success_message = None

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.delete_success_message:
            messages.success(self.request, self.delete_success_message)
        return response


class TeamListView(ListView):
    model = TeamMember
    template_name = "team/team.html"
    context_object_name = "team"


class TeamGenerateDataView(View):
    def post(self, request, *args, **kwargs):
        TeamDataFabric.generate_team_data(amount=20)
        messages.success(request, "20 team members with resumes and contacts were generated.")
        return redirect("team:team")


class TeamDetailView(DetailView):
    model = TeamMember
    template_name = "team/teamMemberDetail.html"
    context_object_name = "teamMember"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["resume"] = getattr(self.object, "resume", None)
        return context


class TeamEditView(MessageOnFormMixin, UpdateView):
    model = TeamMember
    template_name = "team/teamMemberEdit.html"
    context_object_name = "teamMember"
    fields = "__all__"
    success_url = reverse_lazy("team:team")
    success_message = "Team member updated successfully."


class TeamDeleteView(MessageOnDeleteMixin, PermissionRequiredMixin, DeleteView):
    model = TeamMember
    template_name = "team/teamMemberDelete.html"
    context_object_name = "teamMember"
    success_url = reverse_lazy("team:team")
    permission_required = "team.delete_teammember"
    delete_success_message = "Team member deleted successfully."


class TeamCreateView(MessageOnFormMixin, CreateView):
    model = TeamMember
    fields = "__all__"
    template_name = "team/teamMemberCreate.html"
    permission_required = "team.create_team"
    success_url = reverse_lazy("team:team")
    success_message = "Team member created successfully."


class TeamResumeDetailView(DetailView):
    model = Resume
    template_name = "team/teamResumeDetail.html"
    context_object_name = "resume"

    def get_object(self, queryset=None):
        return get_object_or_404(Resume, team_member_id=self.kwargs["member_pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teamMember"] = self.object.team_member
        return context


class TeamResumeListView(ListView):
    model = Resume
    template_name = "team/teamResumeList.html"
    context_object_name = "resumes"

    def get_queryset(self):
        return Resume.objects.select_related("team_member").all()


class TeamResumeCreateView(MessageOnFormMixin, CreateView):
    model = Resume
    template_name = "team/teamResumeForm.html"
    fields = ["position", "summary", "experience_years", "education", "skills"]
    permission_required = "team.create_team"
    success_message = "Resume created successfully."

    def dispatch(self, request, *args, **kwargs):
        self.team_member = get_object_or_404(TeamMember, pk=self.kwargs["member_pk"])
        if hasattr(self.team_member, "resume"):
            return redirect("team:resume_detail", member_pk=self.team_member.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.team_member = self.team_member
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("team:resume_detail", kwargs={"member_pk": self.team_member.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teamMember"] = self.team_member
        context["form_mode"] = "Create"
        return context


class TeamResumeUpdateView(UpdateView):
    model = Resume
    template_name = "team/teamResumeForm.html"
    context_object_name = "resume"
    fields = ["position", "summary", "experience_years", "education", "skills"]
    success_message = "Resume updated successfully."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update resume. Please check the form.")
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(Resume, team_member_id=self.kwargs["member_pk"])

    def get_success_url(self):
        return reverse_lazy("team:resume_detail", kwargs={"member_pk": self.object.team_member.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teamMember"] = self.object.team_member
        context["form_mode"] = "Update"
        return context


class TeamResumeDeleteView(MessageOnDeleteMixin, DeleteView):
    model = Resume
    template_name = "team/teamResumeDelete.html"
    context_object_name = "resume"
    delete_success_message = "Resume deleted successfully."

    def get_object(self, queryset=None):
        return get_object_or_404(Resume, team_member_id=self.kwargs["member_pk"])

    def get_success_url(self):
        return reverse_lazy("team:team_detail", kwargs={"pk": self.kwargs["member_pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teamMember"] = self.object.team_member
        return context


class TeamContactDetailView(DetailView):
    model = Contact
    template_name = "team/teamContactDetail.html"
    context_object_name = "contact"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Contact,
            pk=self.kwargs["contact_pk"],
            team_member_id=self.kwargs["member_pk"],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teamMember"] = self.object.team_member
        return context


class TeamContactCreateView(MessageOnFormMixin, CreateView):
    model = Contact
    template_name = "team/teamContactForm.html"
    fields = ["address", "home_phone", "mobile_phone", "email"]
    success_message = "Contact created successfully."

    def dispatch(self, request, *args, **kwargs):
        self.team_member = get_object_or_404(TeamMember, pk=self.kwargs["member_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.team_member = self.team_member
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("team:team_detail", kwargs={"pk": self.team_member.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teamMember"] = self.team_member
        context["form_mode"] = "Create"
        return context


class TeamContactUpdateView(UpdateView):
    model = Contact
    template_name = "team/teamContactForm.html"
    context_object_name = "contact"
    fields = ["address", "home_phone", "mobile_phone", "email"]
    success_message = "Contact updated successfully."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update contact. Please check the form.")
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(
            Contact,
            pk=self.kwargs["contact_pk"],
            team_member_id=self.kwargs["member_pk"],
        )

    def get_success_url(self):
        return reverse_lazy("team:team_detail", kwargs={"pk": self.kwargs["member_pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teamMember"] = self.object.team_member
        context["form_mode"] = "Update"
        return context


class TeamContactDeleteView(MessageOnDeleteMixin, DeleteView):
    model = Contact
    template_name = "team/teamContactDelete.html"
    context_object_name = "contact"
    delete_success_message = "Contact deleted successfully."

    def get_object(self, queryset=None):
        return get_object_or_404(
            Contact,
            pk=self.kwargs["contact_pk"],
            team_member_id=self.kwargs["member_pk"],
        )

    def get_success_url(self):
        return reverse_lazy("team:team_detail", kwargs={"pk": self.kwargs["member_pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teamMember"] = self.object.team_member
        return context

