from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dashboard.models import Order, Product, Information
from dashboard.forms import ProductForm, ProductEditFormStaff
from .forms import StaffRegisterForm
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
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import os

def staff_register(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to database yet
            user.is_active = False # Wait for manager to activate account
            user.is_staff = True  # Set is_staff to True
            user.save()  # Now save to database
            username = user.username
            messages.success(request, f'Account has been created for {username}.\
                            Your account is pending approval.\
                            You will receive an email once your account is activated.')
            return redirect('user-login')
    else:
        form = StaffRegisterForm()

    helper = FormHelper()
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Sign Up', css_class='btn-primary'))

    return render(request, 'staff/staff_application.html', {'form': form, 'helper': helper})
    
    


def activate(request, pk):
    user = User.objects.get(id=pk)
    user.is_active = True
    user.save()
    message = f'Your account has been activated. You can now login to your account.'
    subject = 'Account Activation'
    # no html message just the plain text
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=True,
    )
    messages.success(request, f'{user.username} has been activated')
    return redirect('dashboard-staff')

@login_required
def staff(request):
    workers=User.objects.filter(is_superuser=False, is_staff=True)
    workers_count=workers.count()
    info = Information.objects.first() if Information.objects.exists() else ""
    orders_count=Order.objects.count()
    products_count=Product.objects.count()
    context={
        'workers':workers,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
        'information_content': info,
    }
    return render(request, 'staff/staff.html',context)

@login_required
def logout_view(request):
    logout(request)
    # return redirect('dashboard-index')
    return render(request, 'user/logout.html')

@login_required
def product(request):
    items=Product.objects.all()
    products_count=Product.objects.count()
    information = Information.objects.first()
    information_content = information.content if information else ""
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name=form.cleaned_data.get('name')
            
            product_new = Product.objects.get(name=product_name)
            barcode_format = 'code128'
            barcode_class = barcode.get_barcode_class(barcode_format)
            product_id = str(product_new.id)
            barcode_image = barcode_class(product_id, writer=ImageWriter())
            barcode_image.save('media/product_barcode/barcode', options={'module_width': 0.5, 'module_height': 15.0, 'font_size': 10})
            product_new.barcode = 'product_barcode/barcode.png'
            product_new.save()

            messages.success(request, f'{product_name} has been added successfully')
            return redirect('staff-product')
        
    form=ProductForm()
    context={
        'items':items,
        'forms':form,
        'products_count':products_count,
        'information_content': information_content,
    }
    return render(request, 'staff/staff_page.html', context)
        
@login_required
def product_delete(request, pk):
    item=Product.objects.get(id=pk)
    if request.method=='POST':
        item.barcode.delete()
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
        form=ProductEditFormStaff(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('staff-product')
    else:
        form=ProductEditFormStaff(instance=item)
    context={
        'form':form
    }
    return render(request, 'staff/staff_update.html', context)

@login_required

def order(request):
    orders=Order.objects.all()
    workers=User.objects.filter(is_superuser=False, is_staff=True)
    workers_count=workers.count()
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