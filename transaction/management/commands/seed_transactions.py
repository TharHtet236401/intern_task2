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
            
            # Categories and their typical amount ranges
            categories = {
                'food': (10, 200),
                'transportation': (5, 100),
                'entertainment': (20, 300),
                'bills': (50, 1000),
                'other': (10, 500)
            }
            
            # Income sources and their typical ranges
            income_sources = {
                'salary': (2000, 5000),
                'freelance': (100, 1000),
                'investment': (50, 500),
                'other': (100, 1000)
            }
            
            # Generate random dates within the last 6 months
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=180)
            
            # Generate 150 transactions (adjust number as needed)
            num_transactions = 150
            transactions = []
            
            for _ in range(num_transactions):
                # Randomly decide if it's income or expense (30% chance of income)
                is_income = random.random() < 0.3
                
                if is_income:
                    category = random.choice(list(income_sources.keys()))
                    min_amount, max_amount = income_sources[category]
                    transaction_type = 'income'
                else:
                    category = random.choice(list(categories.keys()))
                    min_amount, max_amount = categories[category]
                    transaction_type = 'expense'
                
                # Generate random amount with 2 decimal places
                amount = round(random.uniform(min_amount, max_amount), 2)
                
                # Generate random date
                days_between = (end_date - start_date).days
                random_date = start_date + timedelta(days=random.randint(0, days_between))
                
                transaction = Transaction(
                    amount=Decimal(str(amount)),
                    date=random_date,
                    category=category,
                    transaction_type=transaction_type
                )
                transactions.append(transaction)
            
            # Bulk create all transactions
            Transaction.objects.bulk_create(transactions)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {num_transactions} mock transactions')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating mock transactions: {str(e)}')
            ) 