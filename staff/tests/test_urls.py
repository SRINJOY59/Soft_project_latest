from django.test import SimpleTestCase
from django.urls import reverse, resolve
from staff.views import activate
from django.urls import path
from staff import views


class TestUrls(SimpleTestCase):
    
    def test_activate_url_is_resolved(self):
        url=reverse('staff-activate',args=[1])
        print(resolve(url))
        self.assertEqual(resolve(url).func, activate)
        
    def test_staff_url_is_resolved(self):
        url=reverse('dashboard-staff')
        print(resolve(url))
        self.assertEqual(resolve(url).func, views.staff)
        
    def test_staff_page_url_is_resolved(self):
        url=reverse('staff-product')
        print(resolve(url))
        self.assertEqual(resolve(url).func, views.product)
        
    def test_staff_product_update_url_is_resolved(self):
        url=reverse('staff-product-update',args=[1])
        print(resolve(url))
        self.assertEqual(resolve(url).func, views.product_update)
        
    def test_staff_product_delete_url_is_resolved(self):
        url=reverse('staff-product-delete',args=[1])
        print(resolve(url))
        self.assertEqual(resolve(url).func, views.product_delete)
        
    def test_staff_register_url_is_resolved(self):
        url=reverse('staff-application')
        print(resolve(url))
        self.assertEqual(resolve(url).func, views.staff_register)
        
    def test_order_staff_url_is_resolved(self):
        url=reverse('order-staff')
        print(resolve(url))
        self.assertEqual(resolve(url).func, views.order)
        
    def test_order_staff_update_url_is_resolved(self):
        url=reverse('order-staff-update',args=[1])
        print(resolve(url))
        self.assertEqual(resolve(url).func, views.order_update)
        
    def test_product_staff_url_is_resolved(self):
        url=reverse('staff-product')
        print(resolve(url))
        self.assertEqual(resolve(url).func, views.product)
        
        
        