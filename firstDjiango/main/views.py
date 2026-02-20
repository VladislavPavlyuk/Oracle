from django.shortcuts import render

# Create your views here.
def index_view(request):
    return render(request, 'main/index.html',{})


def future_view(request):
    return render(request, 'main/future.html', {})
