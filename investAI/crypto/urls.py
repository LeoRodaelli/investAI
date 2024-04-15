from django.urls import path
from .views import home, nav, login, register

urlpatterns = [
    path('', home, name='home'),
    path('nav/', nav, name='nav'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
]
