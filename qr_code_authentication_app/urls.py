# qr_code_authentication_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.qr_login, name='login'),
    path('fetch-dashboard-data/', views.fetch_dashboard_data, name='fetch_dashboard_data'),
    # Add more URL patterns as needed
]
