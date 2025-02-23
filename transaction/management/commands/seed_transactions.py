from django.core.management.base import BaseCommand
from django.utils import timezone
from transaction.models import Transaction, Budget
import random
from decimal import Decimal
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed the database with mock transactions and budgets'

    def handle(self, *args, **options):
        try:
            # Delete existing data
            Transaction.objects.all().delete()
            Budget.objects.all().delete()
            
            # Define target months
            target_months = [
                (12, 2024),  # December 2024
                (1, 2025),   # January 2025
                (2, 2025),   # February 2025
            ]

            # Set monthly budgets for expense categories
            base_budgets = {
                'food': 800,
                'transportation': 300,
                'entertainment': 400,
                'bills': 1200,
                'other': 500
            }

            # Create budgets for each month with some variation
            for month, year in target_months:
                for category, base_amount in base_budgets.items():
                    # Vary budget by ±10%
                    variation = random.uniform(0.9, 1.1)
                    amount = round(base_amount * variation, 2)
                    Budget.objects.create(
                        category=category,
                        amount=amount,
                        month=month,
                        year=year
                    )

            # Define transaction categories with varying ranges
            expense_categories = {
                'food': {
                    'base_range': (100, 700),  # Most transactions within budget
                    'high_range': (700, 1000),  # Only some will exceed
                    'descriptions': [
                        'Grocery shopping',
                        'Restaurant dinner',
                        'Food delivery',
                        'Cafe and snacks',
                        'Weekly groceries'
                    ]
                },
                'transportation': {
                    'base_range': (30, 250),
                    'high_range': (250, 400),
                    'descriptions': [
                        'Uber ride',
                        'Gas refill',
                        'Car maintenance',
                        'Public transport pass',
                        'Taxi fare'
                    ]
                },
                'entertainment': {
                    'base_range': (50, 300),
                    'high_range': (300, 500),
                    'descriptions': [
                        'Movie tickets',
                        'Concert tickets',
                        'Gaming subscription',
                        'Streaming services',
                        'Weekend activities'
                    ]
                },
                'bills': {
                    'base_range': (200, 1000),  # Most bills within budget
                    'high_range': (1000, 1400),  # Occasional high bills
                    'descriptions': [
                        'Electricity bill',
                        'Water bill',
                        'Internet bill',
                        'Phone bill',
                        'Rent payment'
                    ]
                },
                'other': {
                    'base_range': (50, 400),
                    'high_range': (400, 600),
                    'descriptions': [
                        'Home supplies',
                        'Clothing purchase',
                        'Healthcare expenses',
                        'Gift purchase',
                        'Miscellaneous items'
                    ]
                }
            }

            income_categories = {
                'salary': {
                    'range': (3000, 5000),
                    'descriptions': ['Monthly salary']
                },
                'freelance': {
                    'range': (500, 2000),
                    'descriptions': [
                        'Freelance project',
                        'Consulting work',
                        'Contract payment'
                    ]
                },
                'investment': {
                    'range': (100, 1000),
                    'descriptions': [
                        'Stock dividend',
                        'Interest income',
                        'Investment return'
                    ]
                }
            }

            transactions = []

            # Generate transactions for each month
            for month, year in target_months:
                # Add monthly salary
                salary_amount = round(random.uniform(3000, 5000), 2)
                salary_date = datetime(year, month, random.randint(1, 28)).date()
                
                transactions.append(
                    Transaction(
                        amount=Decimal(str(salary_amount)),
                        date=salary_date,
                        created_at=timezone.now(),
                        category='salary',
                        description='Monthly salary',
                        transaction_type='income'
                    )
                )

                # Generate expenses for each category
                for category in expense_categories:
                    # Lower chance of exceeding budget
                    will_exceed = random.random() < 0.25  # 25% chance to exceed
                    
                    # Vary number of transactions by category
                    if category == 'bills':
                        num_transactions = random.randint(1, 3)  # Fewer bill payments
                    else:
                        num_transactions = random.randint(3, 5)  # Other regular expenses
                    
                    for _ in range(num_transactions):
                        # Determine if this specific transaction will be high
                        is_high = will_exceed and random.random() < 0.5  # Only some transactions will be high
                        
                        amount_range = (
                            expense_categories[category]['high_range'] if is_high 
                            else expense_categories[category]['base_range']
                        )
                        
                        amount = round(random.uniform(*amount_range), 2)
                        day = random.randint(1, 28)
                        date = datetime(year, month, day).date()
                        
                        transactions.append(
                            Transaction(
                                amount=Decimal(str(amount)),
                                date=date,
                                created_at=timezone.now(),
                                category=category,
                                description=random.choice(
                                    expense_categories[category]['descriptions']),
                                transaction_type='expense'
                            )
                        )

                # Add some random income transactions
                for category in ['freelance', 'investment']:
                    if random.random() < 0.7:  # 70% chance of additional income
                        amount = round(random.uniform(
                            *income_categories[category]['range']), 2)
                        day = random.randint(1, 28)
                        date = datetime(year, month, day).date()
                        
                        transactions.append(
                            Transaction(
                                amount=Decimal(str(amount)),
                                date=date,
                                created_at=timezone.now(),
                                category=category,
                                description=random.choice(
                                    income_categories[category]['descriptions']),
                                transaction_type='income'
                            )
                        )

            # Sort transactions by date
            transactions.sort(key=lambda x: x.date)
            
            # Bulk create all transactions
            Transaction.objects.bulk_create(transactions)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {len(transactions)} transactions and '
                    f'{Budget.objects.count()} budgets for Dec 2024 - Feb 2025'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating mock data: {str(e)}')
            ) 