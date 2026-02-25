import random

from django.shortcuts import render
from django.views.generic import TemplateView

PREDICTIONS = [
    "Today is a good day to start what you postponed.",
    "You will receive pleasant news soon.",
    "Your persistence will lead to a strong result.",
    "A new opportunity is close, do not ignore it.",
    "A calm step today will bring big progress tomorrow.",
]


def index_view(request):
    return render(request, "main/index.html", {})


class PredictionView(TemplateView):
    template_name = "main/prediction.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prediction"] = random.choice(PREDICTIONS)
        return context
