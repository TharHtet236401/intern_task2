from django.shortcuts import render, redirect
from .models import Transaction
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import TransactionForm
from django.utils import timezone
import csv
from datetime import datetime
from django.contrib import messages
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
        transactions = Transaction.objects.all().order_by('-date', '-created_at')
        
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
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Transaction added successfully!')
                return redirect('home')
        else:
            form = TransactionForm()
        
        context = {
            'form': form,
            'categories': Transaction.CATEGORY_CHOICES,
            'today': timezone.now().date(),
        }
        return render(request, 'transaction/add_transaction.html', context)
    except Exception as e:
        messages.error(request, str(e))
        return render(request, 'transaction/add_transaction.html', {
            'error': str(e), 
            'categories': Transaction.CATEGORY_CHOICES,
            'today': timezone.now().date()
        })

def export_transactions(request):
    try:
        category = request.GET.get('category', '')
        transactions = Transaction.objects.all().order_by('-date', '-created_at')
        
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

def analysis(request):
    try:
        # Get all transactions
        transactions = Transaction.objects.all()
        
        # Calculate total income and expenses
        total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        
        # Calculate net balance
        net_balance = total_income - total_expenses
        
        context = { 
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance
        }
        
        return render(request, 'transaction/analysis.html', context)
    except Exception as e:
        return render(request, 'transaction/analysis.html', {'error': str(e)})
