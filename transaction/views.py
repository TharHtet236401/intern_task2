from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'transaction/home.html')

def add_transaction(request):
    return render(request, 'transaction/add_transaction.html')

