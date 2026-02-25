from django.shortcuts import render
import random
# Create your views here.
def index_view(request):
    context = {
        'first_value':'first message',
        'second_value': f'Random number: {random.randint(1,100)}',
        'range': range(1, 21)
    }
    return render(request, 'main/index.html',{})

def future_view(request):
    return render(request, 'main/future.html', {})
