from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.models import Product, Order, Information
from datetime import datetime
from unittest.mock import patch, MagicMock
from dashboard.views import generate_barcode, barcode_reader, automated_weighing_machine, edit_information,order_update

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        #User.objects.create_user(username='srinjoydas', password='123@Srinjoy')
        self.user = User.objects.create_user(username='testuser', password='123@Gerimara')
        self.client.login(username='testuser', password='123@Gerimara')

    def test_index_view(self):
        response = self.client.get(reverse('dashboard-index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_add_to_cart_view(self):
        product = Product.objects.create(name='Test Product', quantity=10, selling_price=100, buying_price=50)
        response = self.client.post(reverse('add_to_cart'), {
            'product': product.id,
            'order_quantity': 5,
        })
        self.assertEquals(response.status_code, 302)  

    def test_Cart(self):
        response = self.client.get(reverse('cart'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/cart.html')

    

    def test_generate_barcode_function(self):
        barcode_data = '123456789'
        barcode_image = generate_barcode(barcode_data)
        self.assertTrue(barcode_image)  

    def test_to_counter_view(self):
        Order.objects.create(status='IN_PROGRESS', staff=self.user)
        Order.objects.create(status='IN_PROGRESS', staff=self.user)

        response = self.client.get(reverse('to-counter'))

        cart_orders = Order.objects.filter(status='IN_PROGRESS', staff=self.user)
        self.assertEqual(cart_orders.count(), 0)

        counter_orders = Order.objects.filter(status='WAITING').count()
        self.assertEqual(counter_orders, 2)  

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/counter.html')
    def test_counter_view(self):
    # Create sample orders with different statuses
        Order.objects.create(status='WAITING')
        Order.objects.create(status='WAITING')
        Order.objects.create(status='ACCEPTED')


        response = self.client.get(reverse('counter'))

        counter_orders = Order.objects.filter(status='WAITING').count()
        accepted_orders = Order.objects.filter(status='ACCEPTED').count()
        self.assertEqual(counter_orders, 2)
        self.assertEqual(accepted_orders, 1)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/counter.html')


    def test_automated_weighing_machine(self):
        product = Product.objects.create(name='Test Product', selling_price=100, weight=2)
        order = Order.objects.create(product=product, order_quantity=5)

        # Mocking barcode_reader to return a valid product ID
        with patch('dashboard.views.barcode_reader') as mock_barcode_reader:
            mock_barcode_reader.return_value = product.id
            total_price, total_weight = automated_weighing_machine([order])

        self.assertEqual(total_price, 500)
        self.assertEqual(total_weight, 10)

    def test_checkout_view(self):
        # Create a sample product and order
        product = Product.objects.create(name='Test Product', selling_price=100, weight=2)
        order = Order.objects.create(product=product, order_quantity=5, status='ACCEPTED', staff=self.user)

        # Mocking barcode_reader to return a valid product ID
        with patch('dashboard.views.barcode_reader') as mock_barcode_reader:
            mock_barcode_reader.return_value = product.id
            response = self.client.get(reverse('checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/checkout.html')
        self.assertIn('total_price', response.context)
        self.assertIn('total_weight', response.context)

        # Check if calculated total_price and total_weight match the expected values
        expected_total_price = 500  # 100 * 5
        expected_total_weight = 10  # 2 * 5
        self.assertEqual(response.context['total_price'], expected_total_price)
        self.assertEqual(response.context['total_weight'], expected_total_weight)
    
    def test_billing_view(self):
        # Create sample product and order
        product = Product.objects.create(name='Test Product', selling_price=100, weight=2, quantity=10)
        order = Order.objects.create(product=product, order_quantity=5, status='ACCEPTED', staff=self.user)

        # Mocking automated_weighing_machine to avoid actual calculations
        with patch('dashboard.views.automated_weighing_machine') as mock_automated_weighing_machine:
            mock_automated_weighing_machine.return_value = (500, 10)
            response = self.client.get(reverse('billing'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/billing.html')

        # Check if orders' statuses are updated to 'COMPLETED'
        updated_order = Order.objects.get(id=order.id)
        self.assertEqual(updated_order.status, 'COMPLETED')

        # Check if product's ordered_quantity is updated
        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.ordered_quantity, 5)

        # Check if bill_number is generated
        self.assertIn('bill_number', response.context)
        self.assertTrue(response.context['bill_number'])

        # Check if date is generated
        self.assertIn('date', response.context)
        self.assertTrue(response.context['date'])

        # Check if total_price and total_weight are passed to the context
        self.assertIn('total_price', response.context)
        self.assertEqual(response.context['total_price'], 500)

        self.assertIn('total_weight', response.context)
        self.assertEqual(response.context['total_weight'], 10)

    def test_remove_from_cart_view(self):
        # Create sample product and order
        product = Product.objects.create(name='Test Product', quantity=10)
        order = Order.objects.create(product=product, order_quantity=5, status='IN_PROGRESS', staff=self.user)

        response = self.client.get(reverse('remove_from_cart', kwargs={'product_id': product.id}))
        self.assertEqual(response.status_code, 302)  # Should redirect to 'cart'

        # Check if order is deleted and product quantity is updated
        self.assertFalse(Order.objects.filter(id=order.id).exists())
        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.quantity, 15)  # Initial quantity (10) + removed quantity (5)

    def test_clear_cart_view(self):
        # Create sample product and order
        product = Product.objects.create(name='Test Product', quantity=10)
        order = Order.objects.create(product=product, order_quantity=5, status='IN_PROGRESS', staff=self.user)

        response = self.client.get(reverse('clear_cart'))
        self.assertEqual(response.status_code, 302)  # Should redirect to 'cart'

        # Check if all orders are deleted and product quantities are updated
        self.assertFalse(Order.objects.exists())
        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.quantity, 15)  # Initial quantity (10) + removed quantity (5)

    def test_staff_view(self):
        # Create sample users and data
        User.objects.create_user(username='staff1', password='123@Srinjoy', is_staff=True)
        User.objects.create_user(username='staff2', password='123@Gerimara', is_staff=True)
        Information.objects.create(content='Test information')

        response = self.client.get(reverse('dashboard-staff'))
        self.assertEqual(response.status_code, 200)  # Should return success

        # Check if correct context is passed
        self.assertIn('workers', response.context)
        self.assertIn('workers_count', response.context)
        self.assertIn('orders_count', response.context)
        self.assertIn('products_count', response.context)
        self.assertIn('information_content', response.context)

    def test_staff_detail_view(self):
        # Create sample users and data
        User.objects.create_user(username='staff1', password='password1', is_staff=True)
        User.objects.create_user(username='staff2', password='password2', is_staff=True)
        Information.objects.create(content='Test information')

        response = self.client.get(reverse('dashboard-staff-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)  # Should return success

        # Check if correct context is passed
        self.assertIn('information_content', response.context)
        self.assertIn('workers', response.context)
        self.assertIn('workers_count', response.context)
        self.assertIn('orders_count', response.context)
        self.assertIn('products_count', response.context)

    def test_product_view(self):
        response = self.client.get(reverse('dashboard-product'))
        self.assertEqual(response.status_code, 200)  # Should return success

        # Check if correct context is passed
        self.assertIn('information_content', response.context)
        self.assertIn('items', response.context)
        self.assertIn('form', response.context)
        self.assertIn('workers_count', response.context)
        self.assertIn('orders_count', response.context)
        self.assertIn('products_count', response.context)

    def test_product_create_post(self):
        data = {
            'name': 'Test Product',
            'category': 'Electronics',  # Choose a category from the choices defined in your model
            'quantity': 10,
            'ordered_quantity': 4,
            'buying_price': 100,  # Set the buying price according to your requirement
            'selling_price': 150,  # Set the selling price according to your requirement
    # 'barcode': You might want to provide an actual image file for the barcode field
            'weight': 0.5,  # Set the weight according to your requirement
        }
        response = self.client.post(reverse('dashboard-product'), data=data)
        self.assertEqual(response.status_code, 302)  # Should redirect to 'dashboard-product'

        # Check if product is created
        self.assertTrue(Product.objects.filter(name='Test Product').exists())

    def test_product_delete_view(self):
        product = Product.objects.create(name='Test Product', quantity=10)
        response = self.client.get(reverse('dashboard-product-delete', kwargs={'pk': product.id}))
        self.assertEqual(response.status_code, 200)  

        self.assertIn('item', response.context)

    def test_sales_statistics(self):
        product1 = Product.objects.create(name='Product 1', quantity=10, ordered_quantity=5, buying_price=40, selling_price=50)
        product2 = Product.objects.create(name='Product 2', quantity=20, ordered_quantity=10, buying_price=80, selling_price=100)
        order1 = Order.objects.create(product=product1)
        order2 = Order.objects.create(product=product2)

        response = self.client.get(reverse('sales_statistics'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/sales_statistics.html')
    
    def test_edit_information_view_get(self):
        # Create a request object
        response = self.client.get(reverse('edit-information'))


        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/edit_information.html')

    def test_edit_information_view_post(self):
        data = {'content': 'Updated Content'}
        response = self.client.post(reverse('edit-information'), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard-index'))
        information = Information.objects.first()
        self.assertEqual(information.content, 'Updated Content')

    def test_edit_information_view_invalid_form(self):

        data = {'content': ''}
        response = self.client.post(reverse('edit-information'), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/edit_information.html')

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertIn('content', form.errors)
        self.assertIn('This field is required.', form.errors['content'])


    def test_edit_information_view_nonexistent_instance(self):
        Information.objects.all().delete()
        request = RequestFactory().get(reverse('edit-information'))
        request.user = self.user
        response = edit_information(request)


        self.assertEqual(response.status_code, 200)

    def test_product_update_admin_get(self):
        # Create a product object
        product = Product.objects.create(name='Test Product', quantity=10)
        self.client.login(username='sb', password='adc@12345')
        response = self.client.get(reverse('dashboard-product-update', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/product_update.html')

    def test_product_update_admin_post(self):
        # Create a product object
        product = Product.objects.create(name='Test Product', selling_price=200)
        self.client.login(username='sb', password='adc@12345')
        data = {'selling_price': 220}
        response = self.client.post(reverse('dashboard-product-update', kwargs={'pk': product.pk}), data)
        self.assertEqual(response.status_code, 200)
        product.refresh_from_db()
        self.assertEqual(product.selling_price, 200)

    def test_product_update_staff_get(self):
        # Create a product object
        product = Product.objects.create(name='Test Product', quantity=10)
        self.client.login(username='Srinjoy', password='123@Gerimara')
        response = self.client.get(reverse('dashboard-product-update', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/product_update.html')

    def test_product_update_staff_post(self):
        # Create a product object
        product = Product.objects.create(quantity=10)
        self.client.login(username='Srinjoy', password='123@Gerimara')
        data = {'quantity': 20}
        response = self.client.post(reverse('dashboard-product-update', kwargs={'pk': product.pk}), data)
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.quantity, 20)

    @patch('dashboard.views.redirect')
    def test_order_update(self, mock_redirect):
        # Create an order object
        order = Order.objects.create(order_quantity=5)
        # Mock the request
        response = self.client.post(reverse('dashboard-order-update', kwargs={'pk': order.pk}))
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.order_quantity, 5)  # Assuming OrderUpdateForm doesn't change the quantity
        #mock_redirect.assert_called_once_with('dashboard-order')