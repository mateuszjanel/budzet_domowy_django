from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import Transaction
from .forms import TransactionForm,CategoryForm

def index(request):
    return render(request,'index.html')

def podstrona(request,param1,param2):
    response = '<b>Parametr 1:</b> ' + param1 + '<br>' + '<b>Parametr 2:</b> ' + param2
    return HttpResponse(response)

def raport(request):
    transactions = Transaction.objects.all()
    context = {'transactions' : transactions}
    return render(request,'raport.html', context)

def dodanie_transakcji(request):
    if request.method == "POST":
        # Czekam na ogarniecie kont i kont użytkownikow
        #form = TransactionForm(request.POST)
        #if form.is_valid():
        #    post = form.save(commit=False)
        #    post.save()
        return redirect('index')
    else:
        form = TransactionForm()
        return render(request, 'dodanie-transakcji.html', {'form':form})

def dodanie_kategorii(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
        return redirect('index')
    else:
        form = CategoryForm()
        return render(request, 'dodanie-kategorii.html', {'form':form})