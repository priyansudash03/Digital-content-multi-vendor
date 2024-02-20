import random
from django.http import JsonResponse,HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.db.models import Sum
import datetime

# Create your views here.


def index(request):
    products = Product.objects.all()
    return render(request,'myApp/index.html',{'products':products})

def detail(request,id):
    product = Product.objects.get(id=id)

    return render(request,"myApp/detail.html",{"product":product})

# def create_checkout(request,id):
#     request_data = json.load(request.body)
#     product = Product.objects.get(id=id)
#     payment_success_view(request,order)

def payment_success_view(request,id):
    product = Product.objects.get(id=id)
    order = OrderDetail()
    order.customer_email = request.user.email
    order.product = product
    order.stripe_payment_intent = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    order.amount = int(product.price)
    order.has_paid=True
    #updating sales stats
    product = Product.objects.get(id=order.product.id)
    product.total_sales_amount += int(product.price)
    product.total_sales += 1
    product.save()
    #updating sales stats
    order.save()

    return render(request,'myApp/payment_success.html',{'order':order})

def payment_failed_view(request):
    return render(request,"myApp/failed.html")

def create_product(request):
    if request.method=='POST':
        product_form=ProductForm(request.POST,request.FILES)
        if product_form.is_valid():
            name = product_form.cleaned_data['name']
            description = product_form.cleaned_data['description']
            price = product_form.cleaned_data['price']
            file = request.FILES['file']
            seller = request.user
            product = Product(name=name,description=description,price=price,file=file,seller=seller)
            product.save()
            return redirect('index')
    product_form = ProductForm()
    return render(request,'myApp/create_product.html',{'product_form':product_form})

def product_edit(request,id):
    product = Product.objects.get(id=id)
    if product.seller != request.user:
        return redirect('invalid')
    product_form = ProductForm(request.POST or None,request.FILES or None,instance=product)
    if request.method=="POST":
        if product_form.is_valid():
            product_form.save()
            return redirect('index')
    return render(request,'myApp/product_edit.html',{"product_form":product_form,'product':product})

def product_delete(request,id):
    product = Product.objects.get(id=id)
    if product.seller != request.user:
        return redirect('invalid')
    product = Product.objects.get(id=id)

    if request.method=='POST':
        product.delete()
        return redirect('index')

    return render(request,'myApp/delete.html',{"product":product})

def dashboard(request):
    products = Product.objects.filter(seller=request.user)
    return render(request,'myApp/dashboard.html',{'products':products})

def register(request):
    if request.method=='POST':
        user_form = UserRegistrationForm(request.POST)
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        return redirect('index')

    user_form = UserRegistrationForm()
    return render(request,'myApp/register.html',{'user_form':user_form})

def invalid(request):
    return render(request,'myApp/invalid.html')

def my_purchases(request):
    orders = OrderDetail.objects.filter(customer_email=request.user.email)
    return render(request,'myApp/purchases.html',{'orders':orders})

def sales(request):
    orders = OrderDetail.objects.filter(product__seller=request.user)
    total_sales = orders.aggregate(Sum('amount'))

    #calculate 365 days sum
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = OrderDetail.objects.filter(product__seller=request.user,created_on__gt=last_year)
    yearly_sales = data.aggregate(Sum('amount'))

    return render(request,'myApp/sales.html',{'total_sales':total_sales,'yearly_sales':yearly_sales})
