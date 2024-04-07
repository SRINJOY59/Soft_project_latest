from django.test import TestCase
from staff.forms import StaffRegisterForm

class TestForms(TestCase):
    
    def test_staff_register_form_valid_data(self):
        form = StaffRegisterForm(data={
            'username':'test',
            'email':'ankan@gmail.com',
            'password1':'Agniva@2004',
            'password2':'Agniva@2004',
        })
        
        self.assertTrue(form.is_valid())
        