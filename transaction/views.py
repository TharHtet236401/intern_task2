from django.shortcuts import render
from .models import Transaction
# Create your views here.
def home(request):
    transactions = Transaction.objects.all()
    context = {
        'transactions': transactions
    }
    return render(request, 'transaction/home.html', context)

def add_transaction(request):
    return render(request, 'transaction/add_transaction.html')

