from django.urls import path
from . import views

urlpatterns = [
   # path('register/',views.register, name="register"),
    path('', views.about, name ="aboutpage"),
    path('myshop', views.myshop, name ="myshop"),
    path('shop', views.shop, name ="shop"),
    path('addproductpage/<str:x_ownerName>', views.addproduct, name ="addproductpage"),
    path('addproduct', views.addproduct, name ="addproduct"),
    path('delete/<str:x_id>', views.delete, name ="delete"),
    path('productpage/<str:x_ownerName>', views.productpage, name ="productpage"),
    path('product_detail/<str:pro_name>', views.product_detail, name ="product_detail"),
    path('searchbar/', views.searchbar, name='searchbar'),
    path('myfavorite', views.myfavorite, name ="myfavorite"),
    path('addmyfavorite/<str:x_id>', views.addmyfavorite, name ="addmyfavorite"),
    path('deletefavorite/<str:x_id>', views.deletefavorite, name ="deletefavorite"),]

