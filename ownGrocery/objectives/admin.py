from django.contrib import admin

from objectives.models import Objective

# Register your models here.

@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ("employee","ref_period")       
    ordering = ("employee",)
    
 
    