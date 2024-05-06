from django.urls import path
from .views import Nav, Home, Login, Register

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('nav/', Nav.as_view(), name='nav'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
]
