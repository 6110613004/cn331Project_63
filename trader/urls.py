from . import views
from django.urls import path , include

urlpatterns = [
    path('', views.index, name = 'index'),
    path('add', views.add_Product, name = 'add'),
    path('delete', views.delete_Product, name = 'delete'),
    path('update', views.update_Product, name = 'update'),
]