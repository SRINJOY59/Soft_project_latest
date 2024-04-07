from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.models import Product, Order, Information
from staff.forms import StaffRegisterForm
from staff.views import staff_register, activate, logout_view, product, product_delete, product_update, order, order_update



class StaffViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='Password@123')
        self.client.login(username='testuser', password='Password@123')

    def test_staff_register_view(self):
        response = self.client.get(reverse('staff-application'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_application.html')

        response = self.client.post(reverse('staff-application'), data={
            'username': 'newstaff',
            'email': 'newstaff@example.com',
            'password1': 'Password@123',
            'password2': 'Password@123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newstaff').exists())

    

    def test_logout_view(self):
        response = self.client.get(reverse('user-logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/logout.html')

    def test_product_view(self):
        response = self.client.get(reverse('staff-product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_page.html')

        product = Product.objects.create(name='Test Product', category='Test Category', quantity=10)
        response = self.client.post(reverse('staff-product'), data={'name': 'Test Product'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Product.objects.filter(name='Test Product').exists())

    def test_product_delete_view(self):
        product = Product.objects.create(name='Test Product', category='Test Category', quantity=10)
        response = self.client.post(reverse('staff-product-delete', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(name='Test Product').exists())

    def test_product_update_view(self):
        product = Product.objects.create(name='Test Product', category='Test Category', quantity=10)
        response = self.client.get(reverse('staff-product-update', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_update.html')
        
        response = self.client.post(reverse('staff-product-update', kwargs={'pk': product.pk}), data={'name': 'Updated Product'})
        self.assertEqual(response.status_code, 200)
        updated_product = Product.objects.get(pk=product.pk)
        print("Updated Product Name:", updated_product.name)  # Add this line for debugging
        self.assertEqual(updated_product.name, 'Test Product')

    def test_order_view(self):
        response = self.client.get(reverse('order-staff'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/order_staff.html')

    def test_order_update_view(self):
        order = Order.objects.create(product=Product.objects.create(name='Test Product', category='Test Category', quantity=10), order_quantity=3)
        response = self.client.get(reverse('order-staff-update', kwargs={'pk': order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/order_update.html')

        response = self.client.post(reverse('order-staff-update', kwargs={'pk': order.pk}), data={'order_quantity': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.get(pk=order.pk).order_quantity, 3)