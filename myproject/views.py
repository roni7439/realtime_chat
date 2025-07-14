from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages


def mysite(request):
    return render(request,'mainpage.html')

def signup_page2(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email id already Exits!!')
            return redirect('signup_page2')
        if User.objects.filter(username=name).exists():
            messages.error(request,'Username already Exits!!')
            return redirect('signup_page2')
        user=User.objects.create_user(
            username=name,
            email=email,
            password=password
        )
        user.save()
        messages.success(request,'Successfully Created')
        return redirect('login_page2')
    return render(request,'signup_page2.html')

def login_page2(request):
    if request.method=='POST':
        name=request.POST.get('name')
        password=request.POST.get('password')
        
        user=authenticate(request,username=name,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login to the Acc')
            return redirect('chatbox')
        else:
            messages.error(request,'Invalid Email or password')
            return redirect('login_page2')
    return render(request,'login_page2.html')
