from django.urls import path
from django.contrib.auth.views import LogoutView
from main.views import PredictionView, index_view, CustomLoginView, CustomRegisterView

urlpatterns = [
    path('', index_view, name='index'),
    path('prediction/', PredictionView.as_view(), name='prediction'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),
]
