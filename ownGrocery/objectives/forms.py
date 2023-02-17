#
# objectives/forms.py
#
from django.forms import ModelForm
from .models import Objective


class ObjectiveForm(ModelForm):

    class Meta:
        model = Objective
        fields = '__all__'
        #fields = ['employee','ref_period','domain','subject','description']