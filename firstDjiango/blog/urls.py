from django.urls import path
from blog.views import post_create, post_list

urlpatterns = [
    path("", post_list, name="blog_list"),
    path("create/", post_create, name="blog_create"),
]
