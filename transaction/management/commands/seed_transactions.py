from django.core.management.base import BaseCommand
from django.utils import timezone
from transaction.models import Transaction
import random
from decimal import Decimal
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed the database with mock transactions'

    def handle(self, *args, **options):
        try:
            # Delete existing transactions
            Transaction.objects.all().delete()
            
            # Categories and their typical amount ranges and descriptions
            expense_categories = {
                'food': {
                    'range': (10, 200),
                    'descriptions': [
                        'Grocery shopping at Walmart',
                        'Lunch at restaurant',
                        'Coffee and breakfast',
                        'Weekly groceries',
                        'Food delivery',
                        'Dinner with friends'
                    ]
                },
                'transportation': {
                    'range': (5, 100),
                    'descriptions': [
                        'Bus ticket',
                        'Uber ride',
                        'Gas refill',
                        'Train ticket',
                        'Car maintenance',
                        'Taxi fare'
                    ]
                },
                'entertainment': {
                    'range': (20, 300),
                    'descriptions': [
                        'Movie tickets',
                        'Concert tickets',
                        'Netflix subscription',
                        'Gaming subscription',
                        'Weekend activities',
                        'Bowling night'
                    ]
                },
                'bills': {
                    'range': (50, 1000),
                    'descriptions': [
                        'Electricity bill',
                        'Water bill',
                        'Internet bill',
                        'Phone bill',
                        'Insurance payment',
                        'Rent payment'
                    ]
                },
                'other': {
                    'range': (10, 500),
                    'descriptions': [
                        'Home supplies',
                        'Personal care items',
                        'Office supplies',
                        'Gift purchase',
                        'Clothing purchase',
                        'Miscellaneous items'
                    ]
                }
            }
            
            # Income sources and their typical ranges
            income_categories = {
                'salary': {
                    'range': (2000, 5000),
                    'descriptions': [
                        'Monthly salary',
                        'Regular paycheck',
                        'Salary deposit',
                        'Wage payment',
                        'Pay period deposit'
                    ]
                },
                'freelance': {
                    'range': (100, 1000),
                    'descriptions': [
                        'Freelance project payment',
                        'Consulting fee',
                        'Contract work',
                        'Project completion payment',
                        'Freelance gig'
                    ]
                },
                'investment': {
                    'range': (50, 500),
                    'descriptions': [
                        'Stock dividend',
                        'Interest income',
                        'Investment return',
                        'Portfolio gains',
                        'Dividend payment'
                    ]
                },
                'other': {
                    'range': (100, 1000),
                    'descriptions': [
                        'Gift received',
                        'Refund',
                        'Bonus payment',
                        'Side hustle income',
                        'Miscellaneous income'
                    ]
                }
            }
            
            # Generate random dates within the last 6 months
            end_date = timezone.now()
            start_date = end_date - timedelta(days=180)
            
            # Generate 175 transactions (adjust number as needed)
            num_transactions = 175
            transactions = []
            
            for _ in range(num_transactions):
                # Randomly decide if it's income or expense (30% chance of income)
                is_income = random.random() < 0.3
                
                if is_income:
                    category = random.choice(list(income_categories.keys()))
                    category_data = income_categories[category]
                    transaction_type = 'income'
                else:
                    category = random.choice(list(expense_categories.keys()))
                    category_data = expense_categories[category]
                    transaction_type = 'expense'
                
                # Generate random amount with 2 decimal places
                min_amount, max_amount = category_data['range']
                amount = round(random.uniform(min_amount, max_amount), 2)
                
                # Generate random date and time
                random_days = random.randint(0, (end_date - start_date).days)
                random_seconds = random.randint(0, 24*60*60)  # Random time within the day
                transaction_date = start_date + timedelta(days=random_days)
                created_at = transaction_date + timedelta(seconds=random_seconds)
                
                description = random.choice(category_data['descriptions'])
                
                transaction = Transaction(
                    amount=Decimal(str(amount)),
                    date=transaction_date,
                    created_at=created_at,
                    category=category,
                    description=description,
                    transaction_type=transaction_type
                )
                transactions.append(transaction)
            
            # Sort transactions by created_at before bulk create to maintain chronological order
            transactions.sort(key=lambda x: x.created_at)
            
            # Bulk create all transactions
            Transaction.objects.bulk_create(transactions)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {num_transactions} mock transactions')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating mock transactions: {str(e)}')
            ) 