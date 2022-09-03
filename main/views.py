from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from . import dash_app


def home(request):
    context = {}
    return render(request, 'main/home.html', context)



def examply(request):
    #return HttpResponse("Example Dahsboard")
    context = {}
    return render(request, 'main/examply.html', context)
