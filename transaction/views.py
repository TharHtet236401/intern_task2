from django.shortcuts import render, redirect
from .models import Transaction
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import TransactionForm
from django.utils import timezone
import csv
from datetime import datetime
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
import json
from django.db.models.functions import TruncMonth

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
        transactions = Transaction.objects.all()
        
        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        net_balance = total_income - total_expenses
        
        # Get expense data by category
        expense_by_category = (
            Transaction.objects.filter(transaction_type='expense')
            .values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        
        # Get income data by category
        income_by_category = (
            Transaction.objects.filter(transaction_type='income')
            .values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        
        # Get monthly trends
        monthly_data = (
            Transaction.objects.annotate(month=TruncMonth('date'))
            .values('month', 'transaction_type')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        # Process monthly data for chart
        months = sorted(set(item['month'].strftime('%Y-%m') for item in monthly_data))
        monthly_income = {item['month'].strftime('%Y-%m'): float(item['total']) 
                        for item in monthly_data if item['transaction_type'] == 'income'}
        monthly_expenses = {item['month'].strftime('%Y-%m'): float(item['total']) 
                          for item in monthly_data if item['transaction_type'] == 'expense'}

        # Prepare data for charts
        trend_labels = json.dumps(months)
        trend_income = json.dumps([monthly_income.get(month, 0) for month in months])
        trend_expenses = json.dumps([monthly_expenses.get(month, 0) for month in months])
        
        # Prepare pie chart data
        expense_labels = json.dumps([Transaction.CATEGORY_CHOICES_DICT.get(item['category'], item['category']) 
                                   for item in expense_by_category])
        expense_data = json.dumps([float(item['total']) for item in expense_by_category])
        
        income_labels = json.dumps([Transaction.CATEGORY_CHOICES_DICT.get(item['category'], item['category']) 
                                  for item in income_by_category])
        income_data = json.dumps([float(item['total']) for item in income_by_category])
        
        context = { 
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'expense_labels': expense_labels,
            'expense_data': expense_data,
            'income_labels': income_labels,
            'income_data': income_data,
            'trend_labels': trend_labels,
            'trend_income': trend_income,
            'trend_expenses': trend_expenses,
        }
        
        return render(request, 'transaction/analysis.html', context)
    except Exception as e:
        return render(request, 'transaction/analysis.html', {'error': str(e)})
