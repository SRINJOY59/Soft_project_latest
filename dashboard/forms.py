from django import forms
from .models import Product, Order, Information

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','category','weight','quantity', 'buying_price', 'selling_price']
        
class OrderForm(forms.ModelForm):
     
    class Meta:
        model=Order
        fields = ['product','order_quantity']       
        
        
        
class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['content']        
        
class OrderUpdateForm(forms.ModelForm):
     
    class Meta:
        model=Order
        fields = ['status']
        
class ProductEditFormStaff(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity']

class ProductEditFormAdmin(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['selling_price', 'image']