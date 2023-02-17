from django.shortcuts import render
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)

# Create your views here.
from django.http import HttpResponse
from .forms import ObjectiveForm


def index(request):
    return HttpResponse("Hello, world. You're at the objectives index.")

# Create your views here.
def objective_view(request):
    form = ObjectiveForm()
    context = {'form': form}
    template_name = 'objective.html'
    return render(request, template_name, context)


# Create your views here. Overzicht van de verschillende objectieven in een lijst
def objective_list_view(request):
    form = ObjectiveForm()
    context = {'form': form}
    template_name = 'objective_list.html'
    return render(request, template_name, context)