# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [    
    path('', views.index, name='index'),    
    path('signin/', views.signin, name='my_signin'),
    path('dashboard/', views.dashboard, name='dashboard')
]

