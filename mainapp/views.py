from django.shortcuts import render, redirect
from django.conf import settings
 
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import datetime

from django.views.generic import ListView
 

def index(request):
    if request.user.is_authenticated:
        accounts = Account.objects.filter(user = request.user).values()
        request.session['accounts'] = list(accounts)
        for i in request.session['accounts']:
            i['balance'] = str(i['balance'])
        return render(request,'index.html')
    else:
        return render(request,'registration/login.html')

@login_required
def raport(request):
    if request.session.has_key('current_account'):
        transactions = Transaction.objects.filter(user = request.user,account = request.session.get('current_account')['id']).values()
        for trans in transactions:
            trans['account_id'] = Account.objects.get(pk=trans['account_id']).name
            trans['categories_id'] = Category.objects.get(pk=trans['categories_id']).name
        context = {'transactions' : list(transactions)}
        return render(request,'raport.html', context)
    else:
        return redirect('index')

@login_required
def raportAll(request):
    transactions = Transaction.objects.filter(user = request.user).values()
    for trans in transactions:
        trans['account_id'] = Account.objects.get(pk=trans['account_id']).name
        trans['categories_id'] = Category.objects.get(pk=trans['categories_id']).name
    context = {'transactions': list(transactions)}
    return render(request,'raportAll.html', context)

@login_required
def zlecenia_stale(request):
    standOrds = StandingOrder.objects.filter(user = request.user).values()
    for stor in standOrds:
        stor['account_id'] = Account.objects.get(pk=stor['account_id']).name
        stor['categories_id'] = Category.objects.get(pk=stor['categories_id']).name
    context = {'standOrds': list(standOrds)}
    return render(request,'zlecenia-stale.html', context)

@login_required
def dodanie_transakcji(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            trans = form.save(commit=False)
            if request.POST['type'] == "Wydatek":
                trans.amount = trans.amount * (-1)
            trans.user = request.user
            trans.account = Account.objects.get(pk=request.session.get('current_account')['id'])
            trans.save()
            acc = trans.account
            acc.balance += trans.amount*Currency.objects.get(pk = trans.currency).rate
            acc.save()
            accounts = Account.objects.filter(user = request.user).values()
            request.session['accounts'] = list(accounts)
            for i in request.session['accounts']:
                i['balance'] = str(i['balance'])

        return redirect('raport')
    else:
        form = TransactionForm()
        return render(request, 'dodanie-transakcji.html', {'form':form})
@login_required
def usuwanie_transakcji(request,id):
    trans = Transaction.objects.get(pk=id)
    acc = trans.account
    acc.balance -= trans.amount*Currency.objects.get(pk = trans.currency).rate
    acc.save()
    trans.delete()

    accounts = Account.objects.filter(user = request.user).values()
    request.session['accounts'] = list(accounts)
    for i in request.session['accounts']:
        i['balance'] = str(i['balance'])

    return redirect('raport')

def usuwanie_zlecenia_stalego(request,id):
    stor = StandingOrder.objects.get(pk=id)
    stor.delete()

    return redirect('zlecenia_stale')

@login_required
def dodanie_zlecenia_stalego(request):
    if request.session.has_key('current_account'): 
        if request.method == "POST": 
            form = StandingOrderForm(request.POST)
            if form.is_valid():
                stor = form.save(commit=False)
                if request.POST['type'] == "Wydatek":
                    stor.amount = stor.amount * (-1)
                stor.user = request.user
                stor.account = Account.objects.get(pk=request.session.get('current_account')['id'])
                stor.save()
            return redirect('zlecenia_stale') 
        else: 
            form = StandingOrderForm() 
            return render(request, 'dodanie-zlecenia-stalego.html', {'form':form})
    else:
        redirect('index') 

@login_required 
def dodanie_kategorii(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.account = Account.objects.get(pk=request.session.get('current_account')['id'])
            cat.save()
        return redirect('index')
    else:
        form = CategoryForm()
        return render(request, 'dodanie-kategorii.html', {'form':form})

@login_required
def usuwanie_kategorii(request,id):
    cat = Category.objects.get(pk=id)
    cat.delete()

    accounts = Account.objects.filter(user = request.user).values()
    request.session['accounts'] = list(accounts)
    for i in request.session['accounts']:
        i['balance'] = str(i['balance'])

    return redirect('raport')

@login_required
def dodanie_konta(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
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

@login_required
def usuwanie_konta(request,id):
    acc = Account.objects.get(pk=id)
    acc.delete()

    del request.session['current_account']
    accounts = Account.objects.filter(user = request.user).values()
    request.session['accounts'] = list(accounts)
    for i in request.session['accounts']:
        i['balance'] = str(i['balance'])

    return redirect('raport')

@login_required
def konto_details(request, id):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.account = Account.objects.get(pk=request.session.get('current_account')['id']) 
            cat.save()
        return redirect('index')
    else:
        form = CategoryForm()
        permissions = Permission.objects.filter(account = id).values()
        categories = Category.objects.filter(account = id).values()
        acc = Account.objects.get(pk=id)
        for perm in permissions:
            perm['user_id'] = User.objects.get(pk=perm['user_id']).username
        for account in request.session['accounts']:
            if account['id'] == id:
                request.session['current_account'] = account
        context = {'permissions' : list(permissions), 'current_account':acc, 'form':form, 'categories':list(categories)} 
        return render(request,'konto_details.html', context)

@login_required
def raport_pdf(request):
    if request.session.has_key('current_account'):
        transactions = Transaction.objects.filter(user = request.user,account = request.session.get('current_account')['id']).values()
        for trans in transactions:
            trans['user_id'] = User.objects.get(pk=trans['user_id']).username
            trans['categories_id'] = Category.objects.get(pk=trans['categories_id']).name
        date  = datetime.date.today()
        context = {'request' : request, 'transactions' : list(transactions), 'date': date}
        return PdfRender.render('raport-pdf.html', params=context)
    else:
        return redirect('index')
        

# def render_pdf_view(request):
#     template_path = 'raport.html'
#     # context = {'myvar': 'this is your template context'}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(Context(context))

#     # create a pdf
#     pisaStatus = pisa.CreatePDF(
#        html, dest=response, link_callback=link_callback)
#     if pisaStatus.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response

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

class PdfRender:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

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
