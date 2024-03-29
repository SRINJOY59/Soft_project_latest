from django import forms
from django.contrib.auth.models import User
from dashboard.models import Product, Information
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','category','quantity', 'buying_price', 'selling_price']
              
        
                
class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity']


class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['content']        


class StaffRegisterForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
