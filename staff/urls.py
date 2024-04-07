from django.urls import path
from . import views


urlpatterns = [
    path('activate/<int:pk>', views.activate, name='staff-activate'),
    path('staff/',views.staff, name='dashboard-staff'),
    path('staff_page/',views.product,name='staff-product'),
    path('staff_product_update/<int:pk>/',views.product_update,name='staff-product-update'),
    path('staff_product_delete/<int:pk>/',views.product_delete,name='staff-product-delete'),
    path('staff-register/', views.staff_register, name = 'staff-application'),
    path('order-staff/', views.order, name = 'order-staff'),
    path('order-staff/update/<int:pk>/',views.order_update, name='order-staff-update'),
    path('product-staff/',views.product, name = 'staff-product'),
]
