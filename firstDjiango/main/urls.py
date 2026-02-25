from django.urls import path

from main.views import PredictionView, index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('prediction/', PredictionView.as_view(), name='prediction'),
]
