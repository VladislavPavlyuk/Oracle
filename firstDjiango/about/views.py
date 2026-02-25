from django.views.generic import TemplateView

from about.services import AboutMemberService


class AboutPageView(TemplateView):
    template_name = "about/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = AboutMemberService.get_members()
        return context
