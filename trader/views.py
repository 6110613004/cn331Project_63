from django.shortcuts import render
from django.shortcuts import render, redirect #ดึงมาจากtemplats
from django.http import HttpResponse, HttpResponseRedirect #เขียนบนกระดาน
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


# Create your views here.
def about(request):
    return render(request,"trader/aboutpage.html")

def test(request):
    return render(request,"trader/test.html")

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
            return HttpResponseRedirect(reverse('aboutpage'))
        else:
            return render(request, 'trader/login.html',{
                'message' : 'Invalid'
            })
    return render(request, 'trader/login.html')

def logout_view(request):
    return render(request, 'trader/login.html')