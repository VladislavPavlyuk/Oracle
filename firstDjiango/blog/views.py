from django.shortcuts import redirect, render
from blog.forms import PostCreateForm
from blog.models import Post


def post_list(request):
    posts = Post.objects.all()
    return render(request, "blog/post_list.html", {"posts": posts})


def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("blog_list")
    else:
        form = PostCreateForm()

    return render(request, "blog/post_create.html", {"form": form})
