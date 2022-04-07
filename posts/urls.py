# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [    
    path('', views.index, name='index'),    
    path('signin/', views.signin, name='my_signin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('articles/', views.ArticleListView.as_view() , name='article-list'),
    path('articles/<int:pk>-<str:slug>/', views.article_detail , name='article-detail'),    
    path('articles/add/', views.article_new, name='article-new'),    
]

