from django.http import HttpResponse
from django.shortcuts import render


def Home(request):
    context = {}


    return render (request, 'home/index.html', context)


