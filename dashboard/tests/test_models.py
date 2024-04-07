from django.test import TestCase
from django.contrib.auth.models import User
from dashboard.models import Product, Order, Information

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Product.objects.create(
            name='Test Product', category='Electronics', quantity=10,
            ordered_quantity=5, buying_price=100, selling_price=200,
            total_selling_price=1000, profit=500, weight=0.5
        )

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_category_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'category')

    # Add more test methods as needed

class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='testuser', password='12345')
        product = Product.objects.create(
            name='Test Product', category='Electronics', quantity=10,
            ordered_quantity=5, buying_price=100, selling_price=200,
            total_selling_price=1000, profit=500, weight=0.5
        )
        Order.objects.create(product=product, staff=user, order_quantity=5, status='IN_PROGRESS')

    def test_calculate_profit(self):
        order = Order.objects.get(id=1)
        expected_profit = (order.product.selling_price - order.product.buying_price) * order.order_quantity
        self.assertEqual(order.calculate_profit(), expected_profit)

    # Add more test methods as needed

class InformationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Information.objects.create(content='Test Information')

    def test_content_label(self):
        information = Information.objects.get(id=1)
        field_label = information._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

    # Add more test methods as needed
