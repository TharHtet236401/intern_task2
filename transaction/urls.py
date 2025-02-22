from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transaction-table/', views.transaction_table, name='transaction_table'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
]
