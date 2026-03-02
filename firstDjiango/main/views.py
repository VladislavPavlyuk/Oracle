import random
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView

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

class CustomLoginView(LoginView):
    template_name = "main/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Logged in successfully.")
        return response


class CustomRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "main/register.html"
    success_url = reverse_lazy("index")
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created successfully.")
        return response
