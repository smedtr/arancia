from django.contrib import admin

from teams.models import OrgUnit, Worker, Supervisor, WorkerSupervisor
from django.utils import timezone
# Register your models here.
 
@admin.register(OrgUnit)
class OrgUnitAdmin(admin.ModelAdmin):
    list_display = ("name","get_short_name","parent","get_no_children","get_children")
    ordering = ("parent",)
    #list_filter = ('starting_at',)
    search_fields = ('name',)
    
    def get_no_children(self, obj):
        return OrgUnit.objects.no_of_children(obj)           
    get_no_children.short_description = "No of Children"

    def get_children(self, obj):      
        return list(OrgUnit.objects.get_children(obj))
    get_children.short_description = "Children"

    def get_short_name(self, obj):        
        return OrgUnit.objects.short_name(obj)
    get_short_name.short_description = "Abrev"

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("name","company","no_of_workers","no_of_current_workers","get_supervisor")       
    ordering = ("name",)
        
    def get_supervisor(self, obj):
        get_supervisor = WorkerSupervisor.objects.get_supervisor(obj)        
        return list(get_supervisor)
    get_supervisor.short_description = "Supervisor"

    def no_of_workers(self,obj):        
        return Worker.objects.no_of_workers()
    no_of_workers.short_description = "Aantal"

    def no_of_current_workers(self,obj):        
        return Worker.objects.no_of_current_workers()
    no_of_current_workers.short_description = "Aantal"
    

@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):  
    list_display = ("employee","get_supervisor_company","get_supervised_team") 
    ordering = ("employee",)
    
    def get_supervisor_company(self, obj):      
        get_supervisor_company = Worker.objects.get_supervisor_company(obj)              
        return list(get_supervisor_company)
    get_supervisor_company.short_description = "Company"   
    
    def get_supervised_team(self, obj):          
        get_supervised_team = WorkerSupervisor.objects.get_supervised_team(obj)             
        return list(get_supervised_team)
    get_supervised_team.short_description = "Team"

@admin.register(WorkerSupervisor)
class WorkerSupervisorAdmin(admin.ModelAdmin):
    list_display = ("worker", "type","supervisor")
    ordering = ("worker",)
    
    
  

