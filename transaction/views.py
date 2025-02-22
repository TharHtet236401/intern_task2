from django.shortcuts import render
from .models import Transaction
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
from datetime import datetime
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
            'page_obj': page_obj,
            'categories': Transaction.CATEGORY_CHOICES
        }

        # Check if it's an HTMX request
        if request.headers.get('HX-Request'):
            return render(request, 'transaction/partials/transaction_table.html', context)
        else:
            # For direct URL access, render the full page
            return render(request, 'transaction/home.html', context)

    except Exception as e:
        if request.headers.get('HX-Request'):
            return render(request, 'transaction/partials/transaction_table.html', {'error': str(e)})
        else:
            return render(request, 'transaction/home.html', {'error': str(e)})

def add_transaction(request):
    try:
        return render(request, 'transaction/partials/add_transaction.html')
    except Exception as e:
        # Handle error appropriately
        return render(request, 'transaction/partials/add_transaction.html', {'error': str(e)})

def export_transactions(request):
    try:
        # Get the same filters as the table
        category = request.GET.get('category', '')
        transactions = Transaction.objects.all().order_by('-date')
        
        if category:
            transactions = transactions.filter(category=category)

        # Create the HttpResponse object with CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'

        # Create CSV writer
        writer = csv.writer(response)
        
        # Write header
        writer.writerow(['Date', 'Category', 'Description', 'Type', 'Amount'])

        # Write data
        for transaction in transactions:
            writer.writerow([
                transaction.date.strftime("%Y-%m-%d"),
                transaction.get_category_display(),
                transaction.description,
                transaction.get_transaction_type_display(),
                f"{'+ ' if transaction.transaction_type == 'income' else '- '}${abs(transaction.amount)}"
            ])

        return response
        
    except Exception as e:
        # In case of error, redirect back with error message
        return HttpResponse(f"Error exporting transactions: {str(e)}", status=500)

