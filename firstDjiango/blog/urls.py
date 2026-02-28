from django.urls import path
from blog.views import post_create, post_delete, post_detail, post_list, post_update

urlpatterns = [
    path("", post_list, name="blog_list"),
    path("create/", post_create, name="blog_create"),
    path("<int:pk>/", post_detail, name="blog_detail"),
    path("<int:pk>/edit/", post_update, name="blog_update"),
    path("<int:pk>/delete/", post_delete, name="blog_delete"),
]
