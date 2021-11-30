from django.shortcuts import render


# Create your views here.
def index(request):
    text = "Hello World"
    context = {
        'context_text': text
    }
    return render(request, 'shop/base.html', context)


def home(request):
    text = "This is the home page"
    context = {
        'context_text': text
    }
    return render(request, 'shop/home.html', context)
