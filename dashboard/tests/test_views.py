from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.models import Product, Order
from dashboard.views import add_to_cart, index, remove_from_cart, clear_cart

class TestViews(TestCase):
    
    def setUp(self):
        # Create a test user
        self.client=Client()
        self.dashboard_url=reverse('dashboard-index')
        self.add_to_cart_url=reverse('add_to_cart')
        self.cart_url=reverse('cart')
        self.to_counter_url=reverse('to-counter')
        self.counter_url=reverse('counter')
        self.checkout_url=reverse('checkout')
        self.billing_url=reverse('billing')
        self.remove_from_cart_url=reverse('remove_from_cart', args=[1])
        self.clear_cart_url=reverse('clear_cart')
        self.staff_url=reverse('dashboard-staff')
        self.product_url=reverse('dashboard-product')
        self.order_url=reverse('dashboard-order')
        self.staff_detail_url=reverse('dashboard-staff-detail', args=[1])
        self.product_delete_url=reverse('dashboard-product-delete', args=[1])
        self.product_update_url=reverse('dashboard-product-update', args=[1])
        self.order_update_url=reverse('dashboard-order-update', args=[1])
        self.sales_statistics_url=reverse('sales_statistics')
        self.edit_information_url=reverse('edit-information')
        
        
        
    def index_GET(self):
        response=self.client.get(reverse('dashboard-index'))
            
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'dashboard/index.html')
            
            
    # def add_to_cart_GET(self):
    #     response=self.client.get(reverse('add_to_cart'))
            
    #     self.assertEquals(response.status_code,200)
    #     self.assertTemplateUsed(response,'dashboard/cart.html')
            
             
            
        
        