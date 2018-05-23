from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse('Oto i widok, elo xD')

def podstrona(request,param1,param2):
    response = '<b>Parametr 1:</b> ' + param1 + '<br>' + '<b>Parametr 2:</b> ' + param2
    return HttpResponse(response)
