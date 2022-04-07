# posts/models.py
# Create your models here.
from django.db import models
from django.utils import timezone
import uuid
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User


class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Article(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    author = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='posts_article')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=timezone.now)    
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager() # The default manager.
    published = PublishedArticleManager() 

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    #def get_queryset(self):
    #    return super(PublishedManager,
    #                 self).get_queryset()\
    #                      .filter(status='published')

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('posts:article-detail', kwargs=kwargs)

class Comment(models.Model):
    article = models.ForeignKey(Article,
                             on_delete=models.CASCADE,
                             related_name='comments_for_article')    
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.article}'
            
  