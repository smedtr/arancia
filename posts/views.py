# posts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.utils import timezone

from .models import Article 
from .forms import ArticleForm, CommentForm

# Create your views here.

def index(request):
  return render(request, 'posts/index.html')

def signin(request):
  return render(request, 'posts/sign-in/index.html')

def dashboard(request):
  return render(request, 'posts/dashboard/index.html')

#########################################################################################################

def article_detail(request, pk, slug):
    article = get_object_or_404(Article.published, pk=pk, slug=slug)
    # List of active comments for this post
    comments = article.comments_for_article.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current article to the comment
            new_comment.article = article
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'posts/articles/article_detail.html', {'article': article,
                                                                  'comments': comments,
                                                                  'new_comment': new_comment,
                                                                  'comment_form': comment_form})

def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.published_date = timezone.now()
            article.save()            
            return redirect('posts:article-detail', pk=article.pk, slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'posts/articles/article_edit.html', {'form': form})

 
class ArticleListView(ListView):
    #queryset = Article.objects.all()
    queryset = Article.published.all()
    context_object_name = 'articles'
    paginate_by = 5
    template_name = 'posts/articles/article_list.html'

def article_list(request):
    object_list = Article.published.all()
    paginator = Paginator(object_list, 5) # 5 posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    return render(request,
                  'posts/articles/article_list.html',
                   {'page': page,
                    'articles': articles})