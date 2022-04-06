# posts/models.py
# Create your models here.
from re import U
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User


class Article(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250,
                            unique=True)
    author = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='posts_article')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        #if not self.slug:
        pub_date = str(self.published_date.year) + "-" + str(self.published_date.month) + "-" + str(self.published_date.day)
        self.slug = slugify( pub_date + "-" + self.title)
        super(Article, self).save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    #def get_absolute_url(self):
    #    return reverse('blog:post_detail',
    #                   args=[self.publish.year,
    #                         self.publish.month,
    #                         self.publish.day, self.slug])

    