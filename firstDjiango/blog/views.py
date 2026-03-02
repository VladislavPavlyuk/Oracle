from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
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
            messages.success(request, "Post created successfully.")
            return redirect("blog_list")
        messages.error(request, "Failed to create post. Please check the form.")
    else:
        form = PostCreateForm()

    return render(request, "blog/post_create.html", {"form": form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostCreateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect("blog_list")
        messages.error(request, "Failed to update post. Please check the form.")
    else:
        form = PostCreateForm(instance=post)

    return render(request, "blog/post_update.html", {"form": form, "post": post})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("blog_list")

    return render(request, "blog/post_delete.html", {"post": post})
