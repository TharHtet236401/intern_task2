from django import forms
from .models import Transaction
from django.utils import timezone
from decimal import Decimal

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'category', 'description', 'transaction_type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future")
        return date

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount == 0 or amount is None:
            raise forms.ValidationError("Amount cannot be zero")
        if amount < 0:
            raise forms.ValidationError("Please use the transaction type to indicate expense/income")
        return amount

