from django.shortcuts import render
from django.shortcuts import render, redirect #ดึงมาจากtemplats
from django.http import HttpResponse, HttpResponseRedirect #เขียนบนกระดาน
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import  UserRegisterForm,ProfileUpdateForm,UserUpdateForm,ProductUpdateForm
from django.contrib import messages
from .models import Product,Profile,Category,Day,Time,place,CATEGORY_CHOICES
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
        'PD' : Product.objects.filter(ownerID = request.user.id ).filter(pStatus=True)}
    )

def shop(request):
    return render(request, 'trader/shop.html',{
        'PD' : Product.objects.exclude(ownerID = request.user.pk ).filter(pStatus=True) ,
        'Category' : CATEGORY_CHOICES
        }
    )

def addproductpage(request):
    return render(request, 'trader/addproduct.html')   

def addproduct(request):
    if request.method == 'POST':
        tempUser = User.objects.get(pk = request.user.pk)
        temp = request.POST.copy()
        tempProduct = Product()
        XXX = temp.get('place1')
        pro_form = ProductUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if pro_form.is_valid():     #Still can't update
            pro_form.save()     #Still can't update
            tempProduct.pName = temp.get('product_name')
            tempProduct.p_detail = temp.get('product_detail') #Detail of product
            tempProduct.p_price = temp.get('product_price')
            tempProduct.category = temp.get('product_cat')
            tempProduct.ownerName = tempUser.first_name   #ชื่อของคนลงขาย
            tempProduct.ownerID = tempUser.pk
            if (temp.get('day1') != None)  and (temp.get('place1') != None) and (temp.get('time1') != None) :
                tempProduct.day1 = temp.get('day1')
                tempProduct.place1 = temp.get('place1')
                tempProduct.time1 = temp.get('time1')
                tempProduct.s1 = True
            if (temp.get('day2') != None)  and (temp.get('place2') != None) and (temp.get('time2') != None) :
                tempProduct.day2 = temp.get('day2')
                tempProduct.place2 = temp.get('place2')
                tempProduct.time2 = temp.get('time2')
                tempProduct.s2 = True
            if (temp.get('day3') != None)  and (temp.get('place3') != None) and (temp.get('time3') != None) :
                tempProduct.day3 = temp.get('day3')
                tempProduct.place3 = temp.get('place3')
                tempProduct.time3 = temp.get('time3')
                tempProduct.s3 = True
            tempProduct.save()
            return redirect('myshop')

    else:   
        pro_form = ProductUpdateForm(instance=request.user.profile)
    return render(request, 'trader/addproduct.html',{
        'pro_form' : pro_form
        ,
        'Category' : CATEGORY_CHOICES
        ,
        'DayList' : Day
        ,
        'Time' : Time
        ,
        'place' : place
        
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
        'PDG' : Product.objects.filter(ownerName = x_ownerName).filter(pStatus = True),
        'XXX' : x_ownerName,
        'ID' :  User.objects.get(first_name = x_ownerName).id
        }
    )

def product_detail(request,pro_name):
    tempProduct = Product.objects.get(pName=pro_name)
    if tempProduct.dealday != "" :
        dataDetail = {
            'status' : False ,
            'product_de' : tempProduct,
            'dealday' :	tempProduct.dealday,
            'dealplace'	:	tempProduct.dealplace ,
            'dealtime' :	tempProduct.dealtime
        }
    else:
        dataDetail = {
            'status' : True ,
            'product_de' : tempProduct,
        }
    return render(request,'trader/product.html',dataDetail)

def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        search_Category = request.GET.get('searchCategory')
        if search_Category == 'All':
            post1 = Product.objects.filter(pName__icontains=search).filter(pStatus = True)
        else:
            post1 = Product.objects.filter(category = search_Category,pName__icontains=search).filter(pStatus = True)
    return render(request, 'trader/searchbar.html', {
        'search' : search,
        'post': post1 
        
        }
        )

def myfavorite(request):
    return render(request, 'trader/myfavorite.html',{
        'MF' : Product.objects.filter(MyFavorite = request.user.id)
    }
    )

def addmyfavorite(request,x_id):
    tempUser = User.objects.get(pk = request.user.pk)
    temp = Product.objects.get(id = x_id)
    temp.MyFavorite.add(tempUser)
    return HttpResponseRedirect(reverse('shop'))

def deletefavorite(request,x_id):
        temp = MyFavorite.objects.filter(id = x_id )
        temp.delete()
        return HttpResponseRedirect(reverse('myfavorite'))

def buy(request,x_id):
    tempProduct = Product.objects.get(id = x_id)
    if request.method == 'POST' and tempProduct.buyerID == "" and tempProduct.ownerID != str(request.user.pk) and tempProduct.pStatus == True: 
        tempProduct.buyerID = request.user.id
        tempProduct.buyerName = request.user.first_name
        deal = request.POST.get('deal')
        if deal == "1":
            tempProduct.dealplace = tempProduct.place1
            tempProduct.dealday = tempProduct.day1
            tempProduct.dealtime = tempProduct.time1
        elif deal == "2":
            tempProduct.dealplace = tempProduct.place2
            tempProduct.dealday = tempProduct.day2
            tempProduct.dealtime = tempProduct.time2
        elif deal == "3":
            tempProduct.dealplace = tempProduct.place3
            tempProduct.dealday = tempProduct.day3
            tempProduct.dealtime = tempProduct.time3
        tempProduct.save()
    return HttpResponseRedirect(reverse('shop'))    

def mydeal(request):
    return render(request, 'trader/mydeal.html',{
        'sell' : Product.objects.filter(ownerID = request.user.pk).filter(pStatus=True),
        'buy' : Product.objects.filter(buyerID = request.user.pk).filter(pStatus=True),
        }
    )
def canceldeal(request,x_id):
    tempProduct = Product.objects.get(id = x_id)
    if tempProduct.pStatus == True :
        tempProduct.buyerID = ""
        tempProduct.buyerName = ""
        tempProduct.dealplace = ""
        tempProduct.dealday = ""
        tempProduct.dealtime = ""
        tempProduct.save()
    return HttpResponseRedirect(reverse('mydeal'))

def confirmdeal(request,x_id):
    tempProduct = Product.objects.get(id = x_id)
    tempProduct.pStatus = False 
    tempProduct.save()
    return HttpResponseRedirect(reverse('mydeal'))

def previoustrades(request,x_id):
    
    return render(request, 'trader/previoustrades.html',{
        'previous_sell' : Product.objects.filter(ownerID = x_id).filter(pStatus = False),
        'previous_buy' : Product.objects.filter(buyerID = x_id).filter(pStatus = False) ,
        
        }
    )

def myprevioustrades(request):
    
    return render(request, 'trader/previoustrades.html',{
        'previous_sell' : Product.objects.filter(ownerID = request.user.pk).filter(pStatus = False),
        'previous_buy' : Product.objects.filter(buyerID = request.user.pk).filter(pStatus = False) ,
        
        }
    )
