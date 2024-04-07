from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard.views import index, product, product_delete, product_update, order, order_update, sales_statistics, edit_information, cart, add_to_cart, to_counter, counter, checkout, billing, remove_from_cart, clear_cart

# urls.py
# from django.urls import path
# from . import views
# from .views import remove_from_cart, clear_cart


# urlpatterns=[
#     path('dashboard/', views.index, name='dashboard-index'),
#     path('product/',views.product, name='dashboard-product'),
#     path('product/delete/<int:pk>/',views.product_delete, name='dashboard-product-delete'),
#     path('product/update/<int:pk>/',views.product_update, name='dashboard-product-update'),
#     path('order/',views.order, name='dashboard-order'),
#     path('order/update/<int:pk>/',views.order_update, name='dashboard-order-update'),
#     path('sales_statistics/', views.sales_statistics, name='sales_statistics'),
#     path('edit-information/', views.edit_information, name='edit-information'),
#     path('cart/', views.cart, name='cart'),
#     path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
#     path('to-counter/', views.to_counter, name='to-counter'),
#     path('counter/', views.counter, name='counter'),
#     path('checkout/', views.checkout, name='checkout'),
#     path('billing/', views.billing, name='billing'),
#      path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
#     path('clear/', clear_cart, name='clear_cart'),
# ]

class TestUrls(SimpleTestCase):
        
        def test_dashboard_index_url_is_resolved(self):
            url=reverse('dashboard-index')
            print(resolve(url))
            self.assertEqual(resolve(url).func, index)
            
        def test_dashboard_product_url_is_resolved(self):
            url=reverse('dashboard-product')
            print(resolve(url))
            self.assertEqual(resolve(url).func, product)
            
        def test_dashboard_product_delete_url_is_resolved(self):
            url=reverse('dashboard-product-delete', args=[1])
            print(resolve(url))
            self.assertEqual(resolve(url).func, product_delete)  
            
            
        def test_dashboard_product_update_url_is_resolved(self):
            url=reverse('dashboard-product-update', args=[1])
            print(resolve(url))
            self.assertEqual(resolve(url).func, product_update)
            
            
        def test_dashboard_order_url_is_resolved(self):
            url=reverse('dashboard-order')
            print(resolve(url))
            self.assertEqual(resolve(url).func, order)
            
            
        def test_dashboard_order_update_url_is_resolved(self):
            url=reverse('dashboard-order-update', args=[1])
            print(resolve(url))
            self.assertEqual(resolve(url).func, order_update)
            
        def test_sales_statistics_url_is_resolved(self):
            url=reverse('sales_statistics')
            print(resolve(url))
            self.assertEqual(resolve(url).func, sales_statistics)
            
        def test_edit_information_url_is_resolved(self):
            url=reverse('edit-information')
            print(resolve(url))
            self.assertEqual(resolve(url).func, edit_information)
            
        def test_cart_url_is_resolved(self):
            url=reverse('cart')
            print(resolve(url))
            self.assertEqual(resolve(url).func, cart)
            
        def test_add_to_cart_url_is_resolved(self):
            url=reverse('add_to_cart')
            print(resolve(url))
            self.assertEqual(resolve(url).func, add_to_cart)
            
        def test_to_counter_url_is_resolved(self):
            url=reverse('to-counter')
            print(resolve(url))
            self.assertEqual(resolve(url).func, to_counter)
            
        def test_counter_url_is_resolved(self):
            url=reverse('counter')
            print(resolve(url))
            self.assertEqual(resolve(url).func, counter)
            
        def test_checkout_url_is_resolved(self):
            url=reverse('checkout')
            print(resolve(url))
            self.assertEqual(resolve(url).func, checkout)
            
        def test_billing_url_is_resolved(self):
            url=reverse('billing')
            print(resolve(url))
            self.assertEqual(resolve(url).func, billing)

        def test_remove_from_cart_url_is_resolved(self):
            url=reverse('remove_from_cart', args=[1])
            print(resolve(url))
            self.assertEqual(resolve(url).func, remove_from_cart)

        def test_clear_cart_url_is_resolved(self):
            url=reverse('clear_cart')
            print(resolve(url))
            self.assertEqual(resolve(url).func, clear_cart)