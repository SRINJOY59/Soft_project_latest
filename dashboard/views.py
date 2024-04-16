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
import time
from django.db.models import Q
from dashboard.models import CATEGORY
import sqlite3
import pandas as pd
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import warnings
from fuzzywuzzy import fuzz
warnings.filterwarnings("ignore")



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
        product.total_selling_price -= product.selling_price * order.order_quantity
        product.profit -= (product.selling_price - product.buying_price) * order.order_quantity
        product.save()
        order.delete()
    return redirect('cart')

@login_required
def clear_cart(request):
    order = Order.objects.filter(staff=request.user,status='IN_PROGRESS')
    for item in order:
        product = Product.objects.get(id=Product.product.id)
        product.quantity += Product.order_quantity
        product.total_selling_price -= product.selling_price * Product.order_quantity
        product.profit -= (product.selling_price - product.buying_price) * Product.order_quantity
        product.save()
    return redirect('cart')

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
    return render(request, 'manager/product_delete.html', context)

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
            form=ProductEditFormAdmin(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                return redirect('dashboard-product')
        else:
            form=ProductEditFormAdmin(instance=item)
        context={
            'form':form
        }
        return render(request, 'manager/product_update.html', context)
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
        return render(request, 'manager/product_update.html', context)
    
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

@login_required
def search_product(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', "")
    products = Product.objects.filter()

    if category:
        products = Product.objects.filter(category=category)

    # take only the category name
    categories = [category[0] for category in CATEGORY]
    if query:
        # products = products.filter(Q(name__icontains=query) |
        #                      Q(category__icontains=query))
        products = products.filter(Q(name__icontains=query) | Q(category__icontains=query) | Q(name__icontains=query, category__icontains=query))

        
    return render(request, 'customer/search_product.html', {'products': products,
                                                'query': query,
                                                'categories': categories,
                                                'category': category})

def get_models():
    with open("dashboard/GOOGLE_API_KEY", "r") as f:
        GOOGLE_API_KEY = f.read().strip()

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name = "gemini-pro")
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)
    return llm, embeddings


def generate_vector_index():
    llm, embeddings = get_models()
    conn = sqlite3.connect("db.sqlite3")
    query = "SELECT * FROM dashboard_product"
    df = pd.read_sql_query(query, conn)
    query1 = "SELECT * FROM dashboard_order"
    df2 = pd.read_sql_query(query1, conn)
    conn.close()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    context = "\n\n".join(str(df.iloc[i]) for i in range(len(df)))
    context1 = "\n\n".join(str(df2.iloc[i]) for i in range(len(df2)))
    texts = text_splitter.split_text(context)
    texts1 = text_splitter.split_text(context1)
    texts = texts + texts1
    vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":1})
    return vector_index

def update_api_key(request):
    if request.method == 'POST':
        api_key = request.POST.get('api_key')
        with open("dashboard/GOOGLE_API_KEY", "w") as f:
            f.write(api_key)
        return redirect('query')
    return render(request, 'manager/change_api_key.html')

def generate_answer(query, vector_index):
    llm, embeddings = get_models()
    relevant_documents = vector_index.get_relevant_documents(query)
    prompt_template = """"You are an expert in handling orders and products in a dashboard system! There are two tables in the SQL database: `dashboard_order` and `dashboard_product`. Let's explore their attributes:\n\nFor `dashboard_order`, the attributes are:\nid,\norder_quantity,\ndate,status,\nstaff_id,\nproduct_id\n\nFor `dashboard_product`, the attributes are:\n- id\n,name\n,category\n,quantity\n,ordered_quantity\n,buying_price\n,selling_price\n,total_selling_price\n,profit,barcode\n,weight\n\nYou're now ready to write SQL queries based on these tables. For example, you could ask:\n\n- How many products were ordered by a specific customer?\n- What is the total price of all products in a certain category?\n- Which product has the highest quantity?\n\nFeel free to craft SQL commands based on these tables and their attributes! Just give the SQL Query, nothing more than that, no other comment and stuff, just SQL","
    ***If product is asked by the user, it is always product name, not id.***
    ***if anything outside the database is asked, then say "This query is not related to Product or Order Database".***
    Context: The user has shared the following information about their situation: {context}.

    Question: The user is asking: {question}.

    Answer:
    """

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )


    stuff_chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
    stuff_answer = stuff_chain(
        {"input_documents": relevant_documents, "question":query}, return_only_outputs = True
        )
    return stuff_answer['output_text']

def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        answer = []
        for row in rows:
            answer.append(row[0])
        conn.close()
        return answer
    except sqlite3.Error as e:
        print("Database error:", e)
        return []
    except Exception as e:
        print("An error occurred:", e)
        return []
    


def query(request):
    context = {}
    vector_index = generate_vector_index()
    if request.method == 'POST':
        query = request.POST.get('query')
        if not query:
            return render(request, 'manager/query.html', {'messages': 'Please enter a query'})
        try:
            answer = generate_answer(query, vector_index)
        except Exception as e:
            # Check for API key limit exceeded error (adapt based on your API library)
            if "limit" in str(e) and ("API" in str(e) or "quota" in str(e)):
                return redirect('change_api_key')
            else:
                context['messages'] = "An error occurred. Please try again."
                return render(request, 'manager/query.html', context)

        final = ""
        for i in range(len(answer)):
            if i >= 6 and i < len(answer)-3:
                final = final + answer[i]
                
        final_answer = read_sql_query(final, "db.sqlite3")
        # print("final_answer: ",final_answer)

        if len(final_answer)==1:
            context = {'answer': final_answer[0], 'query': query}
        elif len(final_answer) > 1:
            # convert all elements of the list to string
            final_answer = [str(ele) for ele in final_answer]
            final_answer = ', '.join(final_answer)
            context = {'answer': final_answer, 'query': query}
        else:
            context = {'answer': "This question is probably not related to Product or Order database.", 'query': query}
        # add messages to context
        context['messages'] = ''
        context['query'] = query
        return render(request, 'manager/query.html', context)
    return render(request, 'manager/query.html',{'messages': ''})

def product_details(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
    }
    return render(request, 'dashboard/product_details.html', context)