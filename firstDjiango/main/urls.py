from django.urls import path

from main.views import future_view, index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('future/', future_view, name='future'),
]
