# Generated by Django 5.0.3 on 2024-04-15 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='product_images/default.png', upload_to='product_images'),
        ),
    ]
