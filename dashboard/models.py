from django.db import models
from django.contrib.auth.models import User
# Create your models here.
CATEGORY=(
    ('Stationary','Stationary'),
    ('Electronics','Electronics'),
    ('Food','Food'),
    ('Clothing','Clothing'),
    ('Furniture','Furniture'),
    ('Others','Others'),
)
class Product(models.Model):
    name=models.CharField(max_length=100, null=True)
    description=models.TextField(null=True, default='')
    category=models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity=models.PositiveIntegerField(null=True)
    ordered_quantity=models.PositiveIntegerField(null=True, default=0)
    buying_price = models.PositiveIntegerField(null = True)
    selling_price = models.PositiveIntegerField(null = True)
    total_selling_price = models.PositiveIntegerField(default=0, null=True)
    profit = models.PositiveIntegerField(default=0, null = True)
    barcode = models.ImageField(upload_to='product_barcode', null=True)
    weight=models.FloatField(null=True)
    image=models.ImageField(default='product_images/default.png',upload_to='product_images')
    
    class Meta:
        verbose_name_plural='Product'
    
    def __str__(self):
        return f'{self.name}'
    

class Order(models.Model):
    
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('WAITING', 'Waiting'),
        ('ACCEPTED', 'Accepted'),
        ('COMPLETED', 'Completed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    
    def calculate_profit(self):
        return (self.product.selling_price - self.product.buying_price) * self.product.ordered_quantity
    
    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'

class Information(models.Model):
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content 
    



       
    
    