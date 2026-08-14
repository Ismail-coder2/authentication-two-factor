from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path('',views.signin_view, name='signin'),
    path('signup/',views.signup_view, name='signup'),
    path('signout/',views.signout_view, name='signout'),
    path('qr-auth-toggle/',views.qr_auth_function, name='qr-auth-toggle'),
    path('activate/<uid64>/<token>',views.activate, name='activate'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset-password'),

]
