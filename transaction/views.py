from django.shortcuts import render, redirect
from .models import Transaction, Budget
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

# this time home page will render the whole page not like previoud task 1 
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
    # prepare the backend to send the data for sectionionl areas of the page.
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
            # send the context for htmx requeest
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
    # this is rendering the simple add transaction page not using htmx
    try:
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Transaction added successfully!')
                return redirect('home')
        else:
            form = TransactionForm()
        # prepare the context to send the data for the page
        context = {
            'form': form,
            'categories': Transaction.CATEGORY_CHOICES,
            # this is to show the current date
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
        # this is to get the category from the url
        # i jsut used AI composer for this part as i have no idea how to exprot the data in csv format and learnt form it .It make the button to down http responese with csv header and content type
        category = request.GET.get('category', '')
        transactions = Transaction.objects.all().order_by('-date', '-created_at')
        
        if category:
            transactions = transactions.filter(category=category)

        # Create the HttpResponse object with CSV header to be downloaded
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'

        # Create CSV writer
        writer = csv.writer(response)
        
        # Write header
        writer.writerow(['Date', 'Category', 'Description', 'Type', 'Amount'])

        # Write data from queryset to the csv file
        for transaction in transactions:
            writer.writerow([
                transaction.date.strftime("%Y-%m-%d"),
                transaction.get_category_display(),
                transaction.description,
                transaction.get_transaction_type_display(),
                f"{'+ ' if transaction.transaction_type == 'income' else '- '}${abs(transaction.amount)}"
            ])
        # send the response to the user to be downloaded
        return response
        
    except Exception as e:
        # In case of error, redirect back with error message
        return HttpResponse(f"Error exporting transactions: {str(e)}", status=500)

# This is the most chllengin and timeconsuming part of this task 2.. i got prety well understanding to  send the data for the pie chart.. but became greedy and tried to use AI composer to generate the trendchart, comparison chart and so on .It became out of my hands I tried hard to understand the logic.Need to take the explanation from AI to understand the logic.and which data we have to send to the frontedn to get the correct output.
def analysis(request):
    try:
        # Get current month and year for budget comparison
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        # Get budgets for current month
        budgets = Budget.objects.filter(
            month=current_month,
            year=current_year
        )
        budget_dict = {budget.category: float(budget.amount) for budget in budgets}
        
        # Get expenses for current month
        expenses_by_category = (
            Transaction.objects.filter(
                transaction_type='expense',
                date__month=current_month,
                date__year=current_year
            )
            .values('category')
            .annotate(total=Sum('amount'))
        )
        expense_dict = {item['category']: float(item['total']) for item in expenses_by_category}
        
        # Prepare comparison data
        categories = set(budget_dict.keys()) | set(expense_dict.keys())
        comparison_data = {
            'categories': json.dumps([Transaction.CATEGORY_CHOICES_DICT.get(cat, cat) for cat in categories]),
            'budget_amounts': json.dumps([budget_dict.get(cat, 0) for cat in categories]),
            'spent_amounts': json.dumps([expense_dict.get(cat, 0) for cat in categories])
        }
        
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
        
        # Add comparison data to your existing context
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
            'comparison_data': comparison_data,
        }
        
        return render(request, 'transaction/analysis.html', context)
    except Exception as e:
        return render(request, 'transaction/analysis.html', {'error': str(e)})

def budget(request):
    try:
        # get the month and year from the filter url
        selected_month = int(request.GET.get('month', timezone.now().month))
        selected_year = int(request.GET.get('year', timezone.now().year))
        
        available_years = Budget.objects.dates('created_at', 'year').values_list('year', flat=True).distinct()
        if not available_years:
            available_years = [timezone.now().year]
            
        # Get budgets for selected month/year
        budgets = Budget.objects.filter(
            month=selected_month,
            year=selected_year
        )
        
        # do the calculation amounts for each category in the selected month of the filter
        spent_amounts = (
            Transaction.objects.filter(
                transaction_type='expense',
                date__year=selected_year,
                date__month=selected_month
            )
            .values('category')
            .annotate(total=Sum('amount'))
        )
        
        # Convert to dictionary for easy lookup
        # just taking the advice from AI for better lookup
        spent_dict = {item['category']: float(item['total']) for item in spent_amounts}
        
        # Add spent amounts and calculate progress for each budget
        for budget in budgets:
            spent = spent_dict.get(budget.category, 0)
            budget.spent_amount = spent
            # calculate the remaining amount by subtracting the spent amount from the budget amount
            budget.remaining = float(budget.amount) - spent
            if float(budget.amount) > 0:
                # calculate the progress by dividing the spent amount by the budget amount and multiplying by 100 with the help of AI code suggestons
                budget.progress = min((spent / float(budget.amount)) * 100, 100)
            else:
                budget.progress = 0
        
        context = {
            'budgets': budgets,
            'current_month': timezone.now().month,
            'current_year': timezone.now().year,
            'selected_month': selected_month,
            'selected_year': selected_year,
            'available_years': available_years,
            'months': [
                {'number': i, 'name': datetime(2000, i, 1).strftime('%B')} 
                for i in range(1, 13)
            ]
        }
        # this is to send the data for the htmx request for showing dynamic content based on filter
        if request.headers.get('HX-Request'):
            return render(request, 'transaction/partials/budget_table.html', context)
        
        return render(request, 'transaction/budget.html', context)
    except Exception as e:
        print(f"Error in budget view: {str(e)}")
        return render(request, 'transaction/budget.html', {'error': str(e)})

def add_budget(request):
    try:
        # this is to add the budget to the database wiht simple form
        if request.method == 'POST':
            category = request.POST.get('category')
            amount = request.POST.get('amount')
            month = request.POST.get('month', timezone.now().month)
            year = request.POST.get('year', timezone.now().year)
            
            # Check if budget already exists for this category/month/year
            existing_budget = Budget.objects.filter(
                category=category,
                month=month,
                year=year
            ).first()
            # if exitsed update the budget
            if existing_budget:
                existing_budget.amount = amount
                existing_budget.save()
                messages.success(request, 'Budget updated successfully!')
            else:
                Budget.objects.create(
                    category=category,
                    amount=amount,
                    month=month,
                    year=year
                )
                messages.success(request, 'Budget created successfully!')
            
            return redirect('budget')
        # prepare the context to send the data for the page
        context = {
            'categories': Budget.CATEGORY_CHOICES,
            'current_month': timezone.now().month,
            'current_year': timezone.now().year,
            'months': [
                {'number': i, 'name': datetime(2000, i, 1).strftime('%B')} 
                for i in range(1, 13)
            ]
        }
        return render(request, 'transaction/add_budget.html', context)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('budget')
