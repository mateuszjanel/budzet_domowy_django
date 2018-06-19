from django import forms
from .models import Transaction, Category, StandingOrder, Account

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('title', 'amount','currency','date','categories',) 

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class StandingOrderForm(forms.ModelForm): 
    class Meta: 
        model = StandingOrder 
        fields = ('title', 'amount', 'currency', 'categories', 'frequency', 'next_date',)

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name',)     