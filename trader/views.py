from django.shortcuts import render
from django.shortcuts import render, redirect #ดึงมาจากtemplats
from django.http import HttpResponse, HttpResponseRedirect #เขียนบนกระดาน
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import  UserRegisterForm,ProfileUpdateForm,UserUpdateForm,ProductUpdateForm
from django.contrib import messages
from .models import Product,Profile
# Create your views here.
def about(request):
    return render(request,"trader/aboutpage.html")



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request ,f'Account created for {username}!')
            return redirect(about)
    else:
        form = UserRegisterForm()
    return render(request, 'trader/register.html',{'form':form})



@login_required
def profile(request): #Render Profile page
    if request.method == 'POST':   
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated !')
            return redirect('profile')
    else:   
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context ={
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'trader/profile.html', context)

def myshop(request):
    return render(request, 'trader/myshop.html',{
        'PD' : Product.objects.filter(owner = request.user.id)}
    )

def shop(request):
    return render(request, 'trader/shop.html',{
        'PD' : Product.objects.all() }
    )

def addproductpage(request):
    return render(request, 'trader/addproduct.html')   

def addproduct(request):
    if request.method == 'POST':
        tempUser = User.objects.get(pk = request.user.pk)
        temp = request.POST.copy()
        tempProduct = Product()
        pro_form = ProductUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if pro_form.is_valid():     #Still can't update
            pro_form.save()     #Still can't update
            tempProduct.pName = temp.get('product_name')
            tempProduct.p_detail = temp.get('product_detail') #Detail of product
            tempProduct.p_price = temp.get('product_price')
            tempProduct.ownerName = tempUser.first_name   #ชื่อของคนลงขาย
            tempProduct.save()
            tempOwner = User.objects.get(pk = request.user.pk) 
            tempProduct.owner.add(tempOwner)
            return redirect('myshop')

    else:   
        pro_form = ProductUpdateForm(instance=request.user.profile)
    return render(request, 'trader/addproduct.html',{
        'pro_form':pro_form
    })  
              

def update_ownerName(request):
    tempUser = User.objects.get(pk = request.user.pk)
    tempUser.ownerName = tempUser.first_name

def delete(request,x_id):
        temp = Product.objects.filter(id = x_id )
        temp.delete()
        return HttpResponseRedirect(reverse('myshop'))


def productpage(request,x_ownerName):
    return render(request, 'trader/productpage.html',{
        'PDG' : Product.objects.filter(ownerName = x_ownerName),
        'XXX' : x_ownerName}
    )

def product_detail(request,pro_name):
    return render(request,'trader/product.html',{
        'product_de' : Product.objects.get(pName=pro_name),
    })
def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post1 = Product.objects.filter(pName = search)
    
        return render(request, 'trader/searchbar.html', {'post': post1})

