from django.shortcuts import render
from shop.models import product
from cart.models import cart,order_table,account
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def cart_view(request):
    u=request.user
    total=0
    c=cart.objects.filter(user=u)
    for i in c:
        total=total+i.quantity*i.product.price

    return render(request,'cart.html',{'c':c,'total':total})

@login_required

def addtocart(request,p):
    p=product.objects.get(id=p)
    u=request.user
    try:
        Cart=cart.objects.get(user=u,product=p)
        if(p.stock>0):
            Cart.quantity+=1
            Cart.save()
            p.stock-=1
            p.save()
    except:

        Cart=cart.objects.create(product=p,user=u,quantity=1)
        Cart.save()
        p.stock-=1
        p.save()
    return cart_view(request)
@login_required

def cart_remove(request,p):
    p=product.objects.get(id=p)
    u=request.user
    try:
        Cart=cart.objects.get(user=u,product=p)
        if (Cart.quantity>1):
            Cart.quantity-=1
            Cart.save()
            p.stock+=1
            p.save()
        else:
            Cart.delete()
            p.stock+=1
            p.save()

    except:
        pass
    return cart_view(request)


def full_remove(request,p):
    p=product.objects.get(id=p)
    u=request.user
    try:
        Cart=cart.objects.get(user=u,product=p)
        Cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass 
    return cart_view(request)

@login_required
def orderform(request):
    if (request.method=="POST"):
        a=request.POST['a']
        p = request.POST['p']
        an = request.POST['n']
        u=request.user
        c=cart.objects.filter(user=u)
        total=0
        for i in c:
            total=total+i.quantity*i.product.price

        try:
            ac=account.objects.get(acctnum=an)
            if(ac.amount >= total):
                ac.amount=ac.amount-total
                ac.save()
                for i in c:
                    o=order_table.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
                    o.save()

                c.delete()
                msg="Order Placed Sucessfully"

                return render(request,'orderdetail.html',{'message':msg})
            else:
                msg="Insufficient Amount.You Cant Place Order"
                return render(request,'orderdetail.html',{'message':msg})
        except:
            pass
    return render(request,'orderform.html')

@login_required
def yourorders(request):
    u=request.user
    s=order_table.objects.filter(user=u)
    return render(request,'yourorders.html',{'s':s})




