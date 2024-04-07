from django.test import TestCase
from django.contrib.auth.models import User
from dashboard.models import Product, Order, Information

class ProductModelTest(TestCase):
    def test_product_str_representation(self):
        product = Product.objects.create(name='Test Product', category='Stationary', quantity=10)
        self.assertEqual(str(product), 'Test Product')

class OrderModelTest(TestCase):
    def test_order_str_representation(self):
        user = User.objects.create(username='testuser')
        product = Product.objects.create(name='Test Product', category='Stationary', quantity=10)
        order = Order.objects.create(product=product, staff=user, order_quantity=5)
        self.assertEqual(str(order), 'Test Product ordered by testuser')

class InformationModelTest(TestCase):
    def test_information_str_representation(self):
        info = Information.objects.create(content='Test Information')
        self.assertEqual(str(info), 'Test Information')
