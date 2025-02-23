from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]
    CATEGORY_CHOICES = [
        # Income categories
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('investment', 'Investment'),
        ('other', 'Other'),
        # Expense categories
        ('food', 'Food'),
        ('transportation', 'Transportation'),
        ('entertainment', 'Entertainment'),
        ('bills', 'Bills'),
        ('other', 'Other')
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(max_length=200, blank=True)
    transaction_type = models.CharField(
        max_length=7,
        choices=TRANSACTION_TYPES,
        default='expense'
    )

    CATEGORY_CHOICES_DICT = dict(CATEGORY_CHOICES)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        # Validate amount
        if self.amount <= 0:
            raise ValidationError("Amount must be positive")
        
        # Validate date - compare with timezone.now().date()
        if self.date > timezone.now().date():
            raise ValidationError("Date cannot be in the future")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation before saving
        if not self.id:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.transaction_type})"


class Budget(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transportation', 'Transportation'),
        ('entertainment', 'Entertainment'),
        ('bills', 'Bills'),
        ('other', 'Other')
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)    
    updated_at = models.DateTimeField(default=timezone.now)
    month = models.IntegerField(default=timezone.now().month)
    year = models.IntegerField(default=timezone.now().year)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.month}/{self.year})"

