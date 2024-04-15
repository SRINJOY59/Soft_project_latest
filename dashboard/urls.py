from django.urls import path
from . import views
from .views import remove_from_cart, clear_cart


urlpatterns=[
    path('dashboard/', views.index, name='dashboard-index'),
    path('product/',views.product, name='dashboard-product'),
    path('product/delete/<int:pk>/',views.product_delete, name='dashboard-product-delete'),
    path('product/update/<int:pk>/',views.product_update, name='dashboard-product-update'),
    path('order/',views.order, name='dashboard-order'),
    path('order/update/<int:pk>/',views.order_update, name='dashboard-order-update'),
    path('sales_statistics/', views.sales_statistics, name='sales_statistics'),
    path('edit-information/', views.edit_information, name='edit-information'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('to-counter/', views.to_counter, name='to-counter'),
    path('counter/', views.counter, name='counter'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing/', views.billing, name='billing'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear/', clear_cart, name='clear_cart'),
    path('search/', views.search_product, name='search_product'),
    path('query/', views.query, name='query'),
    path('change_api_key/', views.update_api_key, name='change_api_key'),
    path('product-details/<int:pk>/', views.product_details, name='product_details'),
]
