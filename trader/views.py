from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Product
# Create your views here.

def index(request):
    return render(request, 'trader/index.html', {'AAA' : Product.objects.all()})


def add_Product(request):
    if request.method == 'POST':
        temp = request.POST.copy()
        tempProduct = Product()
        tempProduct.pName = temp.get('product_name')
        tempProduct.save()
        return render(request, 'trader/index.html', {'AAA' : Product.objects.all()})
        

def delete_Product(request):
    if request.method == 'POST':
        temp = Product.objects.filter(pName = request.POST['product_name'])
        temp.delete()
        return render(request, 'trader/index.html', {'AAA' : Product.objects.all()})

def update_Product(request):
    if request.method == 'POST':
        temp = Product.objects.filter(pName = request.POST['product_name'])
        temp.update(pName = request.POST['update_product_name'])
        return render(request, 'trader/index.html', {'AAA' : Product.objects.all()})