from django.contrib import admin
from .models import Transaction, Budget

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Budget)
