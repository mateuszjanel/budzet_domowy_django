from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Transaction

def index(request):
    return render(request,'index.html')

def podstrona(request,param1,param2):
    response = '<b>Parametr 1:</b> ' + param1 + '<br>' + '<b>Parametr 2:</b> ' + param2
    return HttpResponse(response)

def raport(request):
    transactions = Transaction.objects
    context = {'transactions' : transactions}
    return render(request,'raport.html', context)