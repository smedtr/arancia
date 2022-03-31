from django.shortcuts import render

# Create your views here.

def index(request):
  return render(request, 'posts/index.html')

def signin(request):
  return render(request, 'posts/sign-in/index.html')

def dashboard(request):
  return render(request, 'posts/dashboard/index.html')