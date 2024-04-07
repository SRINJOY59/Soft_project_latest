from django.test import SimpleTestCase
from django.urls import reverse, resolve
from staff.views import staff_register, product, product_delete, product_update, order, order_update, logout_view
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):
    
    def test_staff_register_url_is_resolved(self):
        url=reverse('staff-application')
        print(resolve(url))
        self.assertEqual(resolve(url).func, staff_register)
        
    def test_product_url_is_resolved(self):
        url=reverse('staff-product')
        print(resolve(url))
        self.assertEqual(resolve(url).func, product)
        
    def test_product_delete_url_is_resolved(self):
        url=reverse('staff-product-delete', args=[1])
        print(resolve(url))
        self.assertEqual(resolve(url).func, product_delete)  
        
        
    def test_product_update_url_is_resolved(self):
        url=reverse('staff-product-update', args=[1])
        print(resolve(url))
        self.assertEqual(resolve(url).func, product_update)
        
        
    def test_login_url_is_resolved(self):
        url=reverse('user-login')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)  
        
        
    def test_password_reset_view_url_is_resolved(self):
        url=reverse('password-reset')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)
        
        
    def test_password_reset_done_url_is_resolved(self):
        url=reverse('password_reset_done')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)  
        
    def test_password_reset_confirm_url_is_resolved(self):
        url=reverse('password_reset_confirm', args=[1,2])
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)      
        
    def test_order_url_is_resolved(self):
        url=reverse('order-staff')
        print(resolve(url))
        self.assertEqual(resolve(url).func, order)
        
    def test_order_update_url_is_resolved(self):
        url=reverse('order-staff-update', args=[1])
        print(resolve(url))
        self.assertEqual(resolve(url).func, order_update)
        
    # def test_staff_page_is_resolved(self):
    #     url=reverse('staff-product')
    #     print(resolve(url))
    #     self.assertEqual(resolve(url).func, staff_register)
        
    