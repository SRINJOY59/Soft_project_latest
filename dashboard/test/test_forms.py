from django.test import TestCase
from dashboard.forms import ProductForm, OrderForm, InformationForm, OrderUpdateForm, ProductEditFormStaff, ProductEditFormAdmin

class TestForms(TestCase):
    def test_product_form_valid_data(self):
        form = ProductForm(data={
            'name': 'Test Product',
            'category': 'Food',
            'weight': 10.5,
            'quantity': 100,
            'buying_price': 20,
            'selling_price': 30
        })

        self.assertTrue(form.is_valid())

    def test_product_form_no_data(self):
        form = ProductForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)  # 6 fields in the form


    def test_information_form_valid_data(self):
        form = InformationForm(data={
            'content': 'Test Content'
        })

        self.assertTrue(form.is_valid())

    def test_order_update_form_valid_data(self):
        form = OrderUpdateForm(data={
            'status': 'COMPLETED'
        })

        self.assertTrue(form.is_valid())

    def test_product_edit_form_staff_valid_data(self):
        form = ProductEditFormStaff(data={
            'quantity': 50
        })

        self.assertTrue(form.is_valid())

    def test_product_edit_form_admin_valid_data(self):
        form = ProductEditFormAdmin(data={
            'selling_price': 40
        })

        self.assertTrue(form.is_valid())

    
