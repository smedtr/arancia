from django.contrib import admin

from objectives.models import Objective, ObjectiveResult, ObjMaster, ObjDetails, ObjDetailsResult

# Register your models here.

@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ("employee","owner","ref_period")       
    ordering = ("employee",)

@admin.register(ObjectiveResult)
class ObjectiveResult(admin.ModelAdmin):
    list_display = ("objective",)       
  
@admin.register(ObjMaster)
class ObjectiveMaster(admin.ModelAdmin):
    list_display = ("employee","owner","ref_period","stage","obj_details")  

@admin.register(ObjDetails)
class ObjectiveDetails(admin.ModelAdmin):
    list_display = ("employee","owner","domain","subject",) 

@admin.register(ObjDetailsResult)
class ObjectiveDetailsResult(admin.ModelAdmin):
    list_display = ("objective",)     
