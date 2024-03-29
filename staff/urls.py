from django.urls import path
from . import views


urlpatterns = [
    path('staff-register/', views.staff_register, name = 'staff-application')
]
