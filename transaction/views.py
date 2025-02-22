from django.shortcuts import render
from .models import Transaction
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    try:
        categories = Transaction.CATEGORY_CHOICES
        context = {
            'categories': categories
        }
        return render(request, 'transaction/home.html', context)
    except Exception as e:
        # Handle error appropriately
        return render(request, 'transaction/home.html', {'error': str(e)})

def transaction_table(request):
    try:
        category = request.GET.get('category', '')
        transactions = Transaction.objects.all().order_by('-date')
        
        if category:
            transactions = transactions.filter(category=category)
        
        paginator = Paginator(transactions, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj
        }
        return render(request, 'transaction/partials/transaction_table.html', context)
    except Exception as e:
        # Handle error appropriately
        return render(request, 'transaction/partials/transaction_table.html', {'error': str(e)})

def add_transaction(request):
    try:
        return render(request, 'transaction/partials/add_transaction.html')
    except Exception as e:
        # Handle error appropriately
        return render(request, 'transaction/partials/add_transaction.html', {'error': str(e)})

