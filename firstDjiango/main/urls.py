from django.urls import path
from main.views import PredictionView, index_view, CustomLoginView, CustomRegisterView, logout_view

urlpatterns = [
    path('', index_view, name='index'),
    path('prediction/', PredictionView.as_view(), name='prediction'),
    path('logout/', logout_view, name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),
]
