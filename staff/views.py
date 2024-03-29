from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dashboard.models import Order, Product,Information
from dashboard.forms import OrderForm, ProductForm
from .forms import ProductForm, ProductEditForm, InformationForm, StaffRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from random import randint
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from dashboard.forms import OrderUpdateForm
from dashboard.models import Order


def staff_register(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to database yet
            user.is_staff = True  # Set is_staff to True
            user.save()  # Now save to database
            username = user.username
            messages.success(request, f'Account has been created for {username}')
            return redirect('user-login')
    else:
        form = StaffRegisterForm()

    helper = FormHelper()
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Sign Up', css_class='btn-primary'))

    return render(request, 'staff/staff_application.html', {'form': form, 'helper': helper})


@login_required
def logout_view(request):
    logout(request)
    # return redirect('dashboard-index')
    return render(request, 'user/logout.html')




@login_required
def product(request):
    #items=Product.objects.all()
    items=Product.objects.raw('SELECT * FROM dashboard_product')
    products_count=Product.objects.count()
    information = Information.objects.first()
    information_content = information.content if information else ""
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name=form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added successfully')
            return redirect('staff-product')
    else:
        form=ProductForm()    
    context={
        'items':items,
        'forms':form,
        'products_count':products_count,
        'information_content': information_content
    }
    return render(request, 'staff/staff_page.html', context)

@login_required
def product_delete(request, pk):
    item=Product.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('staff-product')
    context={
        'item':item
    }
    return render(request, 'staff/staff_delete.html', context)

@login_required
def product_update(request, pk):
    item=Product.objects.get(id=pk)
    if request.method=='POST':
        form=ProductEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('staff-product')
    else:
        form=ProductEditForm(instance=item)
    context={
        'form':form
    }
    return render(request, 'staff/staff_update.html', context)

@login_required

def order(request):
    orders=Order.objects.all()
    workers_count=User.objects.all().count()
    orders_count=orders.count()
    products_count=Product.objects.count()
    context={
        'orders':orders,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
    }
    return render(request, 'staff/order_staff.html',context)

@login_required
def order_update(request, pk):
    item=Order.objects.get(id=pk)
    if request.method=='POST':
        form=OrderUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('order-staff')
    else:
        form=OrderUpdateForm(instance=item)
    context={
        'form':form
    }
    return render(request, 'dashboard/order_update.html', context)