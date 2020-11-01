from django.urls import path
from . import views

urlpatterns = [
   # path('register/',views.register, name="register"),
    path('', views.about, name ="aboutpage"),
    path('myshop', views.myshop, name ="myshop"),
    path('shop', views.shop, name ="shop"),
    path('addproductpage', views.addproductpage, name ="addproductpage"),
    path('addproduct', views.addproduct, name ="addproduct"),
    path('delete/<str:x_pName>', views.delete, name ="delete"),
    path('productpage/<str:x_ownerName>', views.productpage, name ="productpage"),]
