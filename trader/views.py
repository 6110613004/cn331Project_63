from django.shortcuts import render
from django.shortcuts import render, redirect #ดึงมาจากtemplats
from django.http import HttpResponse, HttpResponseRedirect #เขียนบนกระดาน
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import  ProfileUpdateForm,UserUpdateForm
from django.contrib import messages
# Create your views here.
def about(request):
    return render(request,"trader/aboutpage.html")

def about_login(request):
    return render(request,"trader/aboutpage_logged.html")


def Register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        newuser = User()
        newuser.username = email
        newuser.first_name = first_name
        newuser.last_name = last_name
        newuser.email = email
        newuser.set_password(password)
        newuser.save()
        #from django.shortcuts import render, redirect
        return redirect(login_view)

    return render(request, 'trader/register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('about_logged'))
        else:
            return render(request, 'trader/login.html',{
                'message' : 'Invalid'
            })
    return render(request, 'trader/login.html')

def logout_view(request):
    logout_view(request)
    return render(request, 'trader/login.html',{
        "message": "Logged out"
    })


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

