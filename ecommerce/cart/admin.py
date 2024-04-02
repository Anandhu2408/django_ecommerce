from django.contrib import admin
from django.http import HttpResponse
from .models import *

# Register your models here.
admin.site.register(cart)
admin.site.register(order_table)
admin.site.register(account)