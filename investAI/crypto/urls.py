from django.urls import path
from .views import  Nav, Home, login, register, homeLogado

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('nav/', Nav.as_view(), name='nav'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('homeLogado/', homeLogado, name='homeLogado')
]
