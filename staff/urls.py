from django.urls import path
from . import views


urlpatterns = [
    path('activate/<int:pk>', views.activate, name='staff-activate'),
]
