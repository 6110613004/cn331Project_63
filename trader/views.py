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
    return render(request, 'trader/myshop.html',{                                             # ไปหน้า myshop.html      
        'PD' : Product.objects.filter(ownerID = request.user.id ).filter(pStatus=True)}       # ส่ง object class Product ที่เป็นของ User ที่ login มา              
    )                                                                                         # (pStatus คือ สถานนะของสินค้า True = ยังไม่ได้ทำการขาย False = ทำการขายเเล้ว)

def shop(request):
    return render(request, 'trader/shop.html',{                                               # ไปหน้า shop.html 
        'PD' : Product.objects.exclude(ownerID = request.user.pk ).filter(pStatus=True) ,     # โดยจะส่งค่า object class Product ทั้งหมดที่ไม่ใช่ของ User ที่ login เข้ามา
        'Category' : CATEGORY_CHOICES                                                         # และส่งข้อมูล Category (เป็น list ใน models.py) ไปด้วย (สำหรับการค้นหาในหน้า shop.html)
        }
    )

def addproductpage(request):                                                                  # ไม่ได้ใช้ !!! ลบได้
    return render(request, 'trader/addproduct.html')                                          # เข้าสู่หน้าเพิ่มสินค้า (addproduct.html)

def addproduct(request):                                                                      # function เพิ่มสินค้า
    if request.method == 'POST':                                                              # ตรวจสอบ method ที่ได้รับจาก addproduct.html 
        tempUser = User.objects.get(pk = request.user.pk)                                     # นำข้อมูลของ User ที่ login เก็บไว้ใน tempUser
        temp = request.POST.copy()                                                            # copy ข้อมูลจาก POST ที่ได้รับมา
        tempProduct = Product()                                                               # ให้ tempProduct เป็น Class Product
        pro_form = ProductUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if pro_form.is_valid():     #Still can't update
            pro_form.save()     #Still can't update
            tempProduct.pName = temp.get('product_name')                                # นำชื่อสินค้าใส่ลงใน field ชื่อ pName ใน tempProduct
            tempProduct.p_detail = temp.get('product_detail') #Detail of product        # นำรายละเอียดสินค้าใส่ลงใน field ชื่อ p_detail ใน tempProduct
            tempProduct.p_price = temp.get('product_price')                             # นำราคาสินค้าใส่ลงใน field ชื่อ p_price ใน tempProduct
            tempProduct.category = temp.get('product_cat')                              # นำหมวดหมู่สินค้าใส่ลงใน field ชื่อ category ใน tempProduct
            tempProduct.ownerName = tempUser.first_name   #ชื่อของคนลงขาย                # นำชื่อคนขายใส่ลงใน field ชื่อ ownerName (ชื่อเจ้าของสินค้า) ใน tempProduct
            tempProduct.ownerID = tempUser.pk                                           # นำ ID (ค่า primary key ของคนขาย) คนขายใส่ลงใน field ชื่อ ownerID ใน tempProduct
            if (temp.get('day1') != None)  and (temp.get('place1') != None) and (temp.get('time1') != None) :    # ตรวจสอบค่า วัน สถานที่ เวลา ที่ใช้ทำการนัดซื้อสินค้าชุดที่ 1 ว่าได้รับครบถ้วนหรือไม่
                tempProduct.day1 = temp.get('day1')                                                              # โดยเมื่อครบจะทำการใส่ค่าลงใน field ชุดที่ 1 ตามลำดับ
                tempProduct.place1 = temp.get('place1')                                                          #
                tempProduct.time1 = temp.get('time1')                                                            #
                tempProduct.s1 = True                                                                            # และจะทำการ set ค่า s1 (ค่า status สำหรับตรวจสอบว่ามีข้อมูลอยู่ใน field ชุดที่ 1)
            if (temp.get('day2') != None)  and (temp.get('place2') != None) and (temp.get('time2') != None) :           # ตรวจสอบค่า วัน สถานที่ เวลา ที่ใช้ทำการนัดซื้อสินค้าชุดที่ 2 ว่าได้รับครบถ้วนหรือไม่
                tempProduct.day2 = temp.get('day2')                                                                     # โดยเมื่อครบจะทำการใส่ค่าลงใน field ชุดที่ 2 ตามลำดับ
                tempProduct.place2 = temp.get('place2')                                                                 #
                tempProduct.time2 = temp.get('time2')                                                                   #
                tempProduct.s2 = True                                                                                   # และจะทำการ set ค่า s2 (ค่า status สำหรับตรวจสอบว่ามีข้อมูลอยู่ใน field ชุดที่ 2)
            if (temp.get('day3') != None)  and (temp.get('place3') != None) and (temp.get('time3') != None) :                   # ตรวจสอบค่า วัน สถานที่ เวลา ที่ใช้ทำการนัดซื้อสินค้าชุดที่ 3 ว่าได้รับครบถ้วนหรือไม่
                tempProduct.day3 = temp.get('day3')                                                                             # โดยเมื่อครบจะทำการใส่ค่าลงใน field ชุดที่ 3 ตามลำดับ
                tempProduct.place3 = temp.get('place3')                                                                         #
                tempProduct.time3 = temp.get('time3')                                                                           #
                tempProduct.s3 = True                                                                                           # และจะทำการ set ค่า s3 (ค่า status สำหรับตรวจสอบว่ามีข้อมูลอยู่ใน field ชุดที่ 3)
            tempProduct.save()                                                      # บันทึกค่าลง DataBase
            return redirect('myshop')                                               # กลับสู่หน้า myshop.html

    else:                                                                           # หากการเข้ามาใน Function นี้เป็นการเข้ามาโดยที่ไม่ได้มีการส่ง method Post มาด้วย
        pro_form = ProductUpdateForm(instance=request.user.profile)                 # จะเข้าสู้หน้า addproduct.html เพื่อทำการเพิ่มสินค้า
    return render(request, 'trader/addproduct.html',{
        'pro_form' : pro_form                                                       #                            
        ,                                 
        'Category' : CATEGORY_CHOICES                                               # ส่งข้อมูล หมวดหมู่ เพื่อสะดวกต่อการเพิ่มสินค้า                          
        ,                                 
        'DayList' : Day                                                             # ส่งข้อมูล วัน เพื่อสะดวกต่อการเพิ่มสินค้า          
        ,                                 
        'Time' : Time                                                               # ส่งข้อมูล เวลา เพื่อสะดวกต่อการเพิ่มสินค้า          
        ,                                 
        'place' : place                                                             # ส่งข้อมูล สถานที่ เพื่อสะดวกต่อการเพิ่มสินค้า          
        
    })  
              

def update_ownerName(request):                          # ยังไม่ได้ใช้
    tempUser = User.objects.get(pk = request.user.pk)   # ยังไม่ได้ใช้
    tempUser.ownerName = tempUser.first_name            # ยังไม่ได้ใช้    

def delete(request,x_id):                                      # Function ลบสินค้า รับค่า x_id(ค่า pk ของสินค้านั้นๆ) มา    
        temp = Product.objects.filter(id = x_id )              # ให้ตัวแปล temp เก็บค่า object ของ Class Product ที่มีค่า pk = x_id ที่ได้รับมา                           
        temp.delete()                                          # ใช้ Function delete เพื่อลบ object นั้นออกจาก DataBase
        return HttpResponseRedirect(reverse('myshop'))         # รีเฟชกลับสู่หน้าเดิม (myshop.html)                               


def productpage(request,x_ownerName):                                                     # Function productpage จะรับชื่อเข้ามา             
    return render(request, 'trader/productpage.html',{                                    # ไปสู่หน้า productpage.html                                     
        'PDG' : Product.objects.filter(ownerName = x_ownerName).filter(pStatus = True),   # นำสินค้าที่ชื่อที่รับเข้ามาเป็นเจ้าของและมีสถานะ pStatus เป็น True ส่งออกไป                                                                    
        'XXX' : x_ownerName,                                                              #              
        'ID' :  User.objects.get(first_name = x_ownerName).id                             #                                              
        }
    )

def product_detail(request,pro_name):                                       # Function product_detail จะรับชื่อสินค้าเข้ามา และโชว์ค่ารายละเอียดของสินค้านั้นๆ              
    tempProduct = Product.objects.get(pName=pro_name)                       # ให้ tempProduct เก็บค่าของ object ที่มีชื่อเดียวกับที่รับเข้ามา                                                    
    if tempProduct.dealday != "" :                                          # ตรวจสอบว่า field dealday เพื่อดูว่ามีวันนัดซื้อสินค้าเเล้ว                                  
        dataDetail = {                                                      # เเละส่งค่า              
            'status' : False ,                                              # status เป็น False                                
            'product_de' : tempProduct,                                     # product_de คือ object ที่ tempProduct เก็บไว้                                       
            'dealday' :	tempProduct.dealday,                                # dealday   เป็นตัวแปรสำหรับเก็บ วัน ที่ใช้สำหรับนัด(เลือกโดยผู้ซื้อ)                                          
            'dealplace'	:	tempProduct.dealplace ,                         # dealplace เป็นตัวแปรสำหรับเก็บ สถานที่ ที่ใช้สำหรับนัด(เลือกโดยผู้ซื้อ)                                                
            'dealtime' :	tempProduct.dealtime                            # dealtime  เป็นตัวแปรสำหรับเก็บ เวลา ที่ใช้สำหรับนัด(เลือกโดยผู้ซื้อ)                                               
        }                                                       
    else:                                                       
        dataDetail = {                                                      # ค่าที่ส่ง              
            'status' : True ,                                               # status เป็น True                               
            'product_de' : tempProduct,                                     # product_de คือ object ที่ tempProduct เก็บไว้                                        
        }                                       
    return render(request,'trader/product.html',dataDetail)                 # ไปสู่หน้า product.html                                

def searchbar(request):                                                                                                 # Functions searchbar (สำหรับการค้นหาสินค้า)                            
    if request.method == 'GET':                                                                                         # ตรวจสอบ method Get                             
        search = request.GET.get('search')                                                                              # นำคำที่ค้นหา มาเก็บในตัวแปร search                               
        search_Category = request.GET.get('searchCategory')                                                             # นำหมวดหมู่ที่ค้นหา มาเก็บในตัวแปร search_Category                             
        if search_Category == 'All':                                                                                    # ตรวจสอบหากค่า search_Category เป็น All                       
            post1 = Product.objects.filter(pName__icontains=search).filter(pStatus = True)                              # ให้ post1 เก็บค่า object Class Product ทั้งหมดที่มีคำที่เก็บในตัวแปร search และมีค่า pStatus = True       
        else:                                                                                                           # ตรวจสอบหากค่า search_Category ไม่ใช่ All 
            post1 = Product.objects.filter(category = search_Category,pName__icontains=search).filter(pStatus = True)   #ให้ post1 เก็บค่า object Class Product ทั้งหมดที่มีคำที่เก็บในตัวแปร search และมีค่า category เหมือนกับค่าใน search_Category และมีค่า pStatus = True       
    return render(request, 'trader/searchbar.html', {                                                                   # ไปสู่หน้า searchbar.html
        'search' : search,                                                                                              # ส่งชื่อสินค้าที่ ค้นหาเข้ามาไปด้วย
        'post': post1                                                                                                   #   ส่ง object Class Product ที่อยู่ใน post1
        
        }
        )

def myfavorite(request):                                                    # Function myfavorite (สำหรับดูสินค้าที่ User ถูกใจ)
    return render(request, 'trader/myfavorite.html',{                       # ไปสู่หน้า myfavorite.html
        'MF' : Product.objects.filter(MyFavorite = request.user.id)         # ส่ง object Class Product ทั้งหมดที่มีค่า MyFavorite เป็น user ที่ login
    }
    )

def addmyfavorite(request,x_id):                                # Function addmyfavorite (สำหรับเพิ่มสินค้าที่ตัวเองชื่นชอบ)
    tempUser = User.objects.get(pk = request.user.pk)           # ให้ tempUser เก็บค่าของ Object Class User ของ User ที่ใช้งานอยู่
    temp = Product.objects.get(id = x_id)                       # ให้ temp เก็บค่าของ Object Class Product ที่ค่า pk ตรงกับ x_id ที่ส่งเข้ามา
    temp.MyFavorite.add(tempUser)                               # ให้ object ที่ temp เก็บ เพิ่ม object ที่ tempUser เก็บ (เนื่องจาก field MyFavorite เป็นเเบบ ManyToMany)
    return HttpResponseRedirect(reverse('shop'))                # รีเฟชหน้า shop.html

def deletefavorite(request,x_id):                           # Function deletefavorite (สำหรับลบสินค้าที่ตัวเองเคยกดชื่นชอบไว้)
        temp = MyFavorite.objects.get(id = x_id )           # ให้ temp เก็บค่าของ Object Class Product ที่ค่า pk ตรงกับ x_id ที่ส่งเข้ามา  
        temp.delete()                                       # ให้ temp ลบ object ที่ตัวมันเองเก็บไว้
        return HttpResponseRedirect(reverse('myfavorite'))  # รีเฟชหน้า myfavorite.html

def buy(request,x_id):                                                                                                                          # Functions buy (สำหรับการซื้อของ)
    tempProduct = Product.objects.get(id = x_id)                                                                                                #ให้ tempProduct เก็บค่าของ Object Class Product ที่ค่า pk ตรงกับ x_id ที่ส่งเข้ามา
    if request.method == 'POST' and tempProduct.buyerID == "" and tempProduct.ownerID != str(request.user.pk) and tempProduct.pStatus == True:  # ตรวจสอบว่า method = post และ มีคนซื้อ สินค้านั้นหรือยัง และ เจ้าของสินค้าที่ต้องการซื้อไม่ใช้คนที่เรียกใช้ และ สินค้ายังไม่ถูกขาย
        tempProduct.buyerID = request.user.id                                                                                                   # ให้ buyerID เก็บค่าผู้ใช้ปัจจุบัน(เนื่องจากเป็นคนซื้อ)
        tempProduct.buyerName = request.user.first_name                                                                                         # ให้buyerName เก็บชื่อคนซื้อ
        deal = request.POST.get('deal')                                                                                                         # ตรวจสอบค่า deal ที่ผู้ซื้อกดเข้ามาตอนซื้อ (เก็บค่าที่บอกว่าผู้ซื้อเลือก วัน สถาน เวลา สำหรับนัดซื้อไหน)
        if deal == "1":                                                                                                                         # หาก deal = 1 แสดงว่าเลือก วัน สถานที่ เวลา ชุดที่ 1 
            tempProduct.dealplace = tempProduct.place1                                                                                          # ให้ตัวแปร dealplace เก็บค่า สถานที่ในชุดที่ 1
            tempProduct.dealday = tempProduct.day1                                                                                              # ให้ตัวแปร dealday เก็บค่า วันในชุดที่ 1
            tempProduct.dealtime = tempProduct.time1                                                                                            # ให้ตัวแปร dealtime เก็บค่า เวลาในชุดที่ 1
        elif deal == "2":                                                                                                                       # หาก deal = 2 แสดงว่าเลือก วัน สถานที่ เวลา ชุดที่ 2 
            tempProduct.dealplace = tempProduct.place2                                                                                          # ให้ตัวแปร dealplace เก็บค่า สถานที่ในชุดที่ 2   
            tempProduct.dealday = tempProduct.day2                                                                                              # ให้ตัวแปร dealday เก็บค่า วันในชุดที่ 2
            tempProduct.dealtime = tempProduct.time2                                                                                            # ให้ตัวแปร dealtime เก็บค่า เวลาในชุดที่ 2 
        elif deal == "3":                                                                                                                       # หาก deal = 3 แสดงว่าเลือก วัน สถานที่ เวลา ชุดที่ 3
            tempProduct.dealplace = tempProduct.place3                                                                                          # ให้ตัวแปร dealplace เก็บค่า สถานที่ในชุดที่ 3       
            tempProduct.dealday = tempProduct.day3                                                                                              # ให้ตัวแปร dealday เก็บค่า วันในชุดที่ 3     
            tempProduct.dealtime = tempProduct.time3                                                                                            # ให้ตัวแปร dealtime เก็บค่า เวลาในชุดที่ 3       
        tempProduct.save()                                                                                                                      # บันทึกค่า object หลังจากเปลี่ยนแปลง
    return HttpResponseRedirect(reverse('shop'))                                                                                                # ไปสู่หน้า shop.html

def mydeal(request):                                                                            # Function mydeal (สำหรับดูว่าเรากำลังซื้อ-ขายสินค้าอะไรอยู่บ้าง)
    return render(request, 'trader/mydeal.html',{                                               #ไปสู่หน้า mydeal.html
        'sell' : Product.objects.filter(ownerID = request.user.pk).filter(pStatus=True),        # ให้ key ชื่อ sell เก็บ object Class Product ที่ขายโดย User ที่เรียกดู
        'buy' : Product.objects.filter(buyerID = request.user.pk).filter(pStatus=True),         # ให้ key ชื่อ buy เก็บ object Class Product ที่กำลังซื้อโดย User ที่เรียกดู
        }
    )
def canceldeal(request,x_id):                               # Function canceldeal (สำหรับยกเลิกการซื้อขายนั้นๆ)
    tempProduct = Product.objects.get(id = x_id)            # ให้ tempProduct เก็บค่าของ Object Class Product ที่ค่า pk ตรงกับ x_id ที่ส่งเข้ามา
    if tempProduct.pStatus == True :                        # ตรวจสอบหากสินค้านั้นยังไม่ถูกขายเสร็จสมบูรณ์
        tempProduct.buyerID = ""                            # ลบค่าใน field buyerID
        tempProduct.buyerName = ""                          # ลบค่าใน field buyerName
        tempProduct.dealplace = ""                          # ลบค่าใน field dealplace
        tempProduct.dealday = ""                            # ลบค่าใน field dealday
        tempProduct.dealtime = ""                           # ลบค่าใน field dealtime
        tempProduct.save()                                  # บันทึกค่าที่เปลี่ยนแปลง
    return HttpResponseRedirect(reverse('mydeal'))          # รีเฟชหน้า mydeal.html

def confirmdeal(request,x_id):                              # Functions confirmdeal (ยืนยันว่าการซื้อขายนั้นสำเร็จ)
    tempProduct = Product.objects.get(id = x_id)            # ให้ tempProduct เก็บค่าของ Object Class Product ที่ค่า pk ตรงกับ x_id ที่ส่งเข้ามา
    tempProduct.pStatus = False                             # ให้ค่า pStatus ของ tempProduct เป็น False 
    tempProduct.save()                                      # บันทึกค่า
    return HttpResponseRedirect(reverse('mydeal'))          # รีเฟชหน้า mydeal.html 

def previoustrades(request,x_id):                                                               # Functions previoustrades (สำหรับดูประวัติการซื้อ-ขาย ของคนอื่นๆ)
    
    return render(request, 'trader/previoustrades.html',{                                       # ไปสู่หน้า previoustrades.html
        'previous_sell' : Product.objects.filter(ownerID = x_id).filter(pStatus = False),       # ให้ key ชื่อ previous_sell เก็บ object Class Product ที่เป็นค่า ownerID = x_id ที่ส่งมา และมีสถานะ pStatus = False(ขายเเล้ว)
        'previous_buy' : Product.objects.filter(buyerID = x_id).filter(pStatus = False) ,       # ให้ key ชื่อ previous_buy เก็บ object Class Product ที่เป็นค่า buyerID = x_id ที่ส่งมา และมีสถานะ pStatus = False(ขายเเล้ว)
        
        }
    )

def myprevioustrades(request):                                                                          # Functions myprevioustrades (สำหรับดูประวัติการซื้อ-ขาย ของฉัน)
    
    return render(request, 'trader/previoustrades.html',{                                               # ไปสู่หน้า previoustrades.html
        'previous_sell' : Product.objects.filter(ownerID = request.user.pk).filter(pStatus = False),    # ให้ key ชื่อ previous_sell เก็บ object Class Product ที่เป็นค่า ownerID = ค่า pk ของ User ที่กำลังใช้งาน และมีสถานะ pStatus = False(ขายเเล้ว)
        'previous_buy' : Product.objects.filter(buyerID = request.user.pk).filter(pStatus = False) ,    # ให้ key ชื่อ previous_buy เก็บ object Class Product ที่เป็นค่า buyerID = ค่า pk ของ User ที่กำลังใช้งาน และมีสถานะ pStatus = False(ขายเเล้ว)
        
        }
    )
