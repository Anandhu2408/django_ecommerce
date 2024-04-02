from django.shortcuts import render,redirect
from django.http import HttpResponse
from shop.models import category,product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def allcategories(request):
    c=category.objects.all()
    return render(request,'category.html',{'c':c})

def allproducts(request,p):
    c=category.objects.get(id=p)# retrievs a particular category
    p=product.objects.filter(category=c)
    return render(request,'product.html',{'c':c,'p':p})

def showdetails(request,p):
    p=product.objects.get(id=p)
    return render(request,'details.html',{'p':p})

def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        e=request.POST['e']
        f=request.POST['f']
        l=request.POST['l']

        if(cp==p):
            user=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
            user.save()
            return allcategories(request)
        else:
            return HttpResponse("passwords are not same")
    return render(request, 'register.html')
def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return allcategories(request)
        else:
            return HttpResponse("invalid credentials")

    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return user_login(request)
