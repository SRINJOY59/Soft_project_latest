"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user import views as user_views
from staff import views as staff_views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('', include('staff.urls')),
    path('register/', user_views.register, name='user-register'),
    path('profile/', user_views.profile, name='user-profile'),
    path('product-staff/', staff_views.product, name = 'staff-product'),
    path('profile/update/', user_views.profile_update, name='user-profile-update'),
    path('', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', user_views.logout_view, name='user-logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password-reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('staff_page/',staff_views.product,name='staff-product'),
    path('staff_product_update/<int:pk>/',staff_views.product_update,name='staff-product-update'),
    path('staff_product_delete/<int:pk>/',staff_views.product_delete,name='staff-product-delete'),
    path('staff-register/', staff_views.staff_register, name = 'staff-application'),
    path('order-staff/', staff_views.order, name = 'order-staff'),
    path('order-staff/update/<int:pk>/',staff_views.order_update, name='order-staff-update'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)