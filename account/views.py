from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .filters import OrderFilter
from .forms import OrderForm,CreateUserForm

# Create your views here.

def loginPage(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username,  password=password)
        
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'Credential did not match..')
    return render(request, 'account/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

def register(request):
    context = {}
    form = CreateUserForm    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created Succes!' + user)
            return redirect('loginPage')
    context['form'] = form
    return render(request, 'account/register.html', context)


@login_required(login_url='loginPage')
def home(request):
    orders = Order.objects.all()
    customer = Customer.objects.all()
    
    total_customers = customer.count()
    total_orders = orders.count()
    delivered =  orders.filter(status='Delivered').count()
    pending =  orders.filter(status='Pending').count()
    
    context = {'orders': orders, 'customer':customer, 'total_orders':total_orders,'delivered':delivered,'pending':pending }
    return render(request, 'account/dashboard.html', context)

@login_required(login_url='loginPage')
def products(request):
    context = {}
    products = Procuts.objects.all()
    context['products'] = products
    return render(request, 'account/products.html', context)


@login_required(login_url='loginPage')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    order = customer.order_set.all()
    total_order = order.count()
    myFilter = OrderFilter(request.GET, queryset=order)
    order = myFilter.qs
    context = {'customer':customer, 'order':order, 'total_order':total_order, 'myFilter':myFilter}
    return render(request, 'account/customer.html',context)


@login_required(login_url='loginPage')
def createOder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    fomrset = OrderFormSet(queryset=Order.objectsf.none() ,instance = customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        fomrset = OrderFormSet(request.POST ,instance=customer)
        if fomrset.is_valid():
            fomrset.save()
            return redirect("/")
    context={'fomrset':fomrset}
    return render(request, 'account/order_form.html',context)

@login_required(login_url='loginPage')
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {'form':form}
    return render(request, 'account/order_form.html',context)


@login_required(login_url='loginPage')
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request, 'account/delete.html',context)

