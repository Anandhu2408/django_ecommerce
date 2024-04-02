from django.shortcuts import render
from shop.models import product
from django.db.models import Q


# Create your views here.
def searchproducts(request):
    p=None
    query=""
    if(request.method=="POST"):
        query=request.POST['q']
        if(query):
            p=product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))


    return render(request,'search.html', {'p':p,'q':query})

