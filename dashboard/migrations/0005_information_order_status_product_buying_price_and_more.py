# Generated by Django 5.0.3 on 2024-03-22 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_order_options_product_ordered_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('not_done', 'NOT COMPLETED'), ('completed', 'COMPLETED')], default='NOT COMPLETED', max_length=30),
        )
    ]
