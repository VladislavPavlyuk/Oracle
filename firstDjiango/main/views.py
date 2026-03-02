import random
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
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
    show_hello = False
    hello_username = ""

    if request.user.is_authenticated and request.session.pop("show_hello_once", False):
        show_hello = True
        hello_username = request.user.username

    return render(
        request,
        "main/index.html",
        {
            "show_hello": show_hello,
            "hello_username": hello_username,
        },
    )


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logged out successfully.")
    return redirect("index")

class PredictionView(TemplateView):
    template_name = "main/prediction.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prediction"] = random.choice(PREDICTIONS)
        return context

class CustomLoginView(LoginView):
    template_name = "main/login.html"

    def form_valid(self, form):
        is_first_login = form.get_user().last_login is None
        response = super().form_valid(form)
        if is_first_login:
            self.request.session["show_hello_once"] = True
        messages.success(self.request, "Logged in successfully.")
        return response


class CustomRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "main/register.html"
    success_url = reverse_lazy("index")
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        self.request.session["show_hello_once"] = True
        messages.success(self.request, "Account created successfully.")
        return response
