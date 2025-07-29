# ip_tracking/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login-attempt/', views.sensitive_login_attempt, name='login_attempt'),
    path('public-data/', views.public_data_view, name='public_data')
]
