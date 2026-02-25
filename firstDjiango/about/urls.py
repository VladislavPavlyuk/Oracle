from django.urls import path

from about.views import AboutPageView

urlpatterns = [
    path("", AboutPageView.as_view(), name="about"),
]
