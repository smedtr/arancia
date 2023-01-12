from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import ContactForm


# Create your views here.
def contact_view(request):
    form = ContactForm()
    context = {'form': form}
    template_name = 'contact.html'
    return render(request, template_name, context)

    