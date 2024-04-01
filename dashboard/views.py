from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Information
from .forms import ProductForm, OrderForm, InformationForm, ProductEditFormStaff, ProductEditFormAdmin, OrderUpdateForm
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from random import randint
from django.shortcuts import render
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import os
from pyzbar.pyzbar import decode
import cv2

# Create your views here.

@login_required
def index(request):
    orders = Order.objects.filter(status='COMPLETED')
    products = Product.objects.all()
    workers=User.objects.filter(is_superuser=False, is_staff=True)
    workers_count=workers.count()
    orders_count = orders.count()
    products_count = Product.objects.count()
    information = Information.objects.first()  # Assuming there's only one instance
    information_content = information.content if information else ""
    # Filter out orders with order_quantity not equal to zero

    total_selling_prices = [product.total_selling_price for product in products]
    profits = [product.profit for product in products]

    in_cart = Order.objects.filter(status='IN_PROGRESS', staff=request.user).count()

    form = OrderForm()

    context = {
        'orders': orders,
        'in_cart': in_cart,
        'form': form,
        'products': products,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
       # 'daily_selling_prices': daily_selling_prices,
        'total_selling_prices': total_selling_prices,
        'profits': profits,
        'information_content': information_content,
    }

    return render(request, 'dashboard/index.html', context)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            product = Product.objects.get(id=form.data['product'])
            order = Order.objects.filter(product=product, status='IN_PROGRESS', staff=request.user).first()
            if int(form.data['order_quantity']) > product.quantity:
                messages.error(request, 'Order quantity exceeds available stock')
            elif order:
                order.order_quantity += int(form.data['order_quantity'])
                product.quantity -= int(form.data['order_quantity'])
                product.total_selling_price += product.selling_price * int(form.data['order_quantity'])
                product.profit += (product.selling_price - product.buying_price) * int(form.data['order_quantity'])
                product.save()
                order.save()
                messages.success(request, 'Added to cart successfully')
            else:
                product.quantity -= int(form.data['order_quantity'])
                product.total_selling_price += product.selling_price * int(form.data['order_quantity'])
                product.profit += (product.selling_price - product.buying_price) * int(form.data['order_quantity'])
                product.save()
                instance.save()
                messages.success(request, 'Added to cart successfully')                
    return redirect('dashboard-index')

@login_required
def cart(request):
    cart_orders = Order.objects.filter(status='IN_PROGRESS', staff=request.user) 
    context = {
        'cart_orders': cart_orders,
        'cart': cart_orders.count(),
    }
    return render(request, 'dashboard/cart.html', context)

@login_required
def to_counter(request):
    cart_orders = Order.objects.filter(status='IN_PROGRESS', staff=request.user)
    for order in cart_orders:
        order.status = 'WAITING'
        order.save()

    counter_orders = Order.objects.filter(status='WAITING').count()
    accepted_orders = Order.objects.filter(status='ACCEPTED')
    context = {
        'counter_orders': counter_orders,
        'accepted_orders': accepted_orders,
    }
    return render(request, 'dashboard/counter.html', context)

@login_required
def counter(request):
    counter_orders = Order.objects.filter(status='WAITING').count()
    accepted_orders = Order.objects.filter(status='ACCEPTED')
    context = {
        'counter_orders': counter_orders,
        'accepted_orders': accepted_orders,
    }
    return render(request, 'dashboard/counter.html', context)

def barcode_reader(barcode_image):
    # Read barcode image
    barcode_image = 'media/' + str(barcode_image)
    image = cv2.imread(barcode_image)
    barcode_data = decode(image)
    if barcode_data:
        return int(barcode_data[0].data.decode())
    return None

def automated_weighing_machine(orders):
    total_price = 0
    total_weight = 0

    for order in orders:
        barcode_image = order.product.barcode
        product_id = barcode_reader(barcode_image)
        product = Product.objects.get(id=product_id)
        total_price += product.selling_price * order.order_quantity
        total_weight += product.weight * order.order_quantity

    return total_price, total_weight

@login_required
def checkout(request):
    accepted_orders = Order.objects.filter(status='ACCEPTED', staff=request.user)
    total_price, total_weight = automated_weighing_machine(accepted_orders)
    context = {
        'total_price': total_price,
        'total_weight': total_weight,
    }
    return render(request, 'dashboard/checkout.html', context)

@login_required
def billing(request):
    accepted_orders = Order.objects.filter(status='ACCEPTED', staff=request.user)
    total_price, total_weight = automated_weighing_machine(accepted_orders)
    for order in accepted_orders:
        order.status = 'COMPLETED'
        product = order.product
        product.ordered_quantity += order.order_quantity
        product.save()
        order.save()

    # use system date and a random number as bill number
    bill_number = f'{datetime.now().strftime("%Y%m%d%H%M%S")}{randint(1000, 9999)}'
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    barcode_format = 'code128'
    barcode_class = barcode.get_barcode_class(barcode_format)
    
    barcode_image = barcode_class(bill_number, writer=ImageWriter())
    barcode_image.save('media/barcode/barcode', options={'module_width': 0.5, 'module_height': 15.0, 'font_size': 10})

    context = {
        'cart_orders': accepted_orders,
        'total_price': total_price,
        'date': date,
        'bill_number': bill_number,
        'total_weight':total_weight,
    }
    return render(request, 'dashboard/billing.html', context)

@login_required
def remove_from_cart(request, product_id):
    order = Order.objects.filter(product_id=product_id, staff=request.user, status='IN_PROGRESS')
    if order.exists():
        order = order.first()
        product = Product.objects.get(id=product_id)
        product.quantity += order.order_quantity
        product.save()
        order.delete()
    return redirect('cart')

@login_required
def clear_cart(request):
    order = Order.objects.filter(staff=request.user,status='IN_PROGRESS')
    for item in order:
        product = Product.objects.get(id=item.product.id)
        product.quantity += item.order_quantity
        product.save()
        item.delete()
    return redirect('cart')

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
    return render(request, 'dashboard/staff.html',context)

@login_required
def staff_detail(request, pk):
    workers=User.objects.filter(is_superuser=False, is_staff=True)
    workers_count=workers.count()
    orders_count=Order.objects.count()
    products_count=Product.objects.count()
    info = Information.objects.first() if Information.objects.exists() else ""
    context={
        'information_content': info,
        'workers':workers,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
    }
    return render(request, 'dashboard/staff_detail.html',context)

@login_required
def product(request):
    items=Product.objects.all()
    info = Information.objects.first() if Information.objects.exists() else ""
    workers=User.objects.filter(is_superuser=False, is_staff=True)
    workers_count=workers.count()
    orders_count=Order.objects.count()
    products_count=Product.objects.count()
    
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
            barcode_image.save(f'media/product_barcode/{product_id}', options={'module_width': 0.5, 'module_height': 15.0, 'font_size': 10})
            product_new.barcode = f'product_barcode/{product_id}.png'
            product_new.save()

            messages.success(request, f'{product_name} has been added successfully')
            return redirect('dashboard-product')
    form=ProductForm()

    context={
        'information_content': info,
        'items':items,
        'form':form,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
    }
    return render(request, 'dashboard/product.html', context)

@login_required
def product_delete(request, pk):
    item=Product.objects.get(id=pk)
    if request.method=='POST':
        os.remove(item.barcode.path)
        item.delete()
        return redirect('dashboard-product')
    context={
        'item':item
    }
    return render(request, 'dashboard/product_delete.html', context)

@login_required
def order(request):
    orders=Order.objects.all()
    workers=User.objects.filter(is_superuser=False, is_staff=True)
    workers_count=workers.count()
    info = Information.objects.first() if Information.objects.exists() else ""
    orders_count=orders.count()
    products_count=Product.objects.count()
    context={
        'information_content': info,
        'orders':orders,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
    }
    return render(request, 'dashboard/order.html',context)

@login_required
def sales_statistics(request):
    orders = Order.objects.all()
    cur_orders = []
    cur_products = set()  # Track unique products
    for order in orders:
        if order.product not in cur_products:
            cur_orders.append(order)
            cur_products.add(order.product)
    statistics = []
    for order in cur_orders:
        profit = order.calculate_profit()
        statistics.append({
            'product': order.product.name,
            'quantity_sold': order.product.ordered_quantity,
            'price_realized': order.product.selling_price,
            'profit': profit,
            'total_selling_price': order.product.ordered_quantity * order.product.selling_price,
        })
    return render(request, 'dashboard/sales_statistics.html', {'statistics': statistics})



def edit_information(request):
    information = Information.objects.first()  # Assuming there's only one instance
    if request.method == 'POST':
        form = InformationForm(request.POST, instance=information)
        if form.is_valid():
            form.save()
            return redirect('dashboard-index')  # Redirect to the dashboard or any other page after successful form submission
    else:
        form = InformationForm(instance=information)
    
    return render(request, 'dashboard/edit_information.html', {'form': form})

@login_required
def product_update(request, pk):
    if request.user.is_superuser:
        item=Product.objects.get(id=pk)
        if request.method=='POST':
            form=ProductEditFormAdmin(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('dashboard-product')
        else:
            form=ProductEditFormAdmin(instance=item)
        context={
            'form':form
        }
        return render(request, 'dashboard/product_update.html', context)
    else:
        item=Product.objects.get(id=pk)
        if request.method=='POST':
            form=ProductEditFormStaff(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('dashboard-product')
        else:
            form=ProductEditFormStaff(instance=item)
        context={
            'form':form
        }
        return render(request, 'dashboard/product_update.html', context)
    
def generate_barcode(data):
    # Generate barcode image
    barcode_image = BytesIO()
    barcode.generate('code128', data, writer=ImageWriter(), output=barcode_image)
    return barcode_image.getvalue()



@login_required
def order_update(request, pk):
    item=Order.objects.get(id=pk)
    if request.method=='POST':
        form=OrderUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-order')
    else:
        form=OrderUpdateForm(instance=item)
    context={
        'form':form
    }
    return render(request, 'dashboard/order_update.html', context)
