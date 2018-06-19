from django.shortcuts import render, redirect
from django.conf import settings
 
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from .forms import TransactionForm,CategoryForm,StandingOrderForm#,RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
 
def index(request):
    return render(request,'index.html')
 
def podstrona(request,param1,param2):
    response = '<b>Parametr 1:</b> ' + param1 + '<br>' + '<b>Parametr 2:</b> ' + param2
    return HttpResponse(response)

@login_required
def raport(request):
    transactions = Transaction.objects.all()
    context = {'transactions' : transactions}
    return render(request,'raport.html', context)

@login_required
def dodanie_transakcji(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            trans = form.save(commit=False)
            trans.user = request.user
            trans.account = request.session['current_account']
            trans.save()

        return redirect('index')
    else:
        form = TransactionForm()
        return render(request, 'dodanie-transakcji.html', {'form':form})

@login_required
def dodanie_zlecenia_stalego(request): 
    if request.method == "POST": 
        # tu też poczekaj na ogarnięcie kont 
        return redirect('index') 
    else: 
        form = StandingOrderForm() 
        return render(request, 'dodanie-zlecenia-stalego.html', {'form':form}) 
@login_required 
def dodanie_kategorii(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.save()
        return redirect('index')
    else:
        form = CategoryForm()
        return render(request, 'dodanie-kategorii.html', {'form':form})

def dodanie_konta(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            acc = form.save(commit=False)
            acc.user = request.user
            acc.balance = 0
            acc.save()
            permission = Permission(user = request.user, account = acc, owner = True)
            permission.save()
        return redirect('index')
    else:
        form = AccountForm()
        return render(request, 'dodanie-konta.html', {'form':form})
 
        
def anonymous_required(view_function, redirect_to = None):
    return AnonymousRequired(view_function, redirect_to)
 
class AnonymousRequired(object):
    def __init__(self, view_function, redirect_to):
        if redirect_to is None:
            redirect_to = settings.LOGIN_REDIRECT_URL
        self.view_function = view_function
        self.redirect_to = redirect_to
 
    def __call__(self, request, *args, **kwargs):
        if request.user is not None and request.user.is_authenticated:
            return HttpResponseRedirect(self.redirect_to)
        return self.view_function(request, *args, **kwargs)
 
# @anonymous_required
# def register(request):
#     register_form = RegistrationForm(request.POST or None,
#         initial={
#             'username': '',
#             'email': '',
#             'password': '',
#             'repeat_password': '',
#         }
#     )
#     if request.method == 'POST':
#         if register_form.is_valid():
#             data = register_form.cleaned_data
 
#             # data.get('username')
#             # data.get('email')
#             # data.get('password')
#             # data.get('repeat_password')
 
#             # Register a new user
#             user = User.objects.create_user(username=data.get('username'),
#                                  email=data.get('email'),
#                                  password=data.get('password'))
 
#     return render(request, 'registration/register.html', context={'register_form': register_form})