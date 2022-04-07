# posts/admin.py
from django.contrib import admin
from .models import Article, Comment

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author','published_date','status')
    list_filter = ('status', 'created_date', 'published_date', 'author')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ('status', 'published_date')# Register your models here.

@admin.register(Comment)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article')
    #list_filter = ('status', 'created_date', 'published_date', 'author')
    search_fields = ('name', 'email','created')
    raw_id_fields = ('article',)
    date_hierarchy = 'created'
    ordering = ('created', 'active')# Register your models here.