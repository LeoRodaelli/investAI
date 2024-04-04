from django.urls import path
from .views import Index, Register, Login, Home

app_name = 'crypto'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('home/', Home.as_view(), name='home'),
]
