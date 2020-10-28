from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.Register, name="register"),
    path('', views.about, name ="aboutpage"),
    path('login_view', views.login_view, name="login_view"),
    path('logout_view', views.logout_view, name="logout_view"),
    path('user/',views.about_login, name = "about_logged"),
    path('profile/', views.profile,name="profile"),
] 