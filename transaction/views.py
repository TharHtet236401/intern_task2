from django.shortcuts import render
from .models import Transaction
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    transactions = Transaction.objects.all().order_by('-date')
    context = {
        'transactions': transactions
    }
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, 'transaction/home.html', context)

def add_transaction(request):
    return render(request, 'transaction/add_transaction.html')

