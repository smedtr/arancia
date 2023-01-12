from django.db import models
from datetime import date, datetime
from django.utils import timezone
from django.utils.timezone import get_current_timezone, make_aware, now
from django.db.models import Q

# Create your models here.

#
class OrgUnitQuerySet(models.QuerySet):
    #    
    # Zie https://spookylukey.github.io/django-views-the-right-way/thin-views.html
    
    def no_of_children(self,obj):        
        return self.filter(parent=obj).count() 

    def short_name(self,obj):
        return(obj.name[-3].upper())       

    def get_children(self, obj):
        children = self.filter(parent=obj).values_list('name')
        return list(children)   

class WorkerQuerySet(models.QuerySet):
    #    
    # Zie https://spookylukey.github.io/django-views-the-right-way/thin-views.html
    
   
    def no_of_workers(self):        
        return self.filter(is_active=True).count()

    def no_of_current_workers(self):  
        # current date       
        now = timezone.now()                   
        # Example 6  https://www.fullstackpython.com/django-utils-timezone-now-examples.html
        tz = get_current_timezone()
        # date taken = 1 Feb 2023
        future_date = make_aware(datetime(
            int(2023),int(2),int(1)),tz)
        # past date = 1 Feb 2022
        past_date = make_aware(datetime(
            int(2022),int(2),int(1)),tz)
        #
        ref_date = now
        #
        no_of_workers = self.filter(Q(is_active=True, 
                                    starting_at__lte=ref_date,
                                    ending_at__isnull=True) |
                                    Q(is_active=True, 
                                    starting_at__lte=ref_date,
                                    ending_at__gte=ref_date) ).count()
        return no_of_workers

    def get_active_workers(self):             
        # current date       
        now = timezone.now()                   
        # Example 6  https://www.fullstackpython.com/django-utils-timezone-now-examples.html
        tz = get_current_timezone()
        # date taken = 1 Feb 2023
        future_date = make_aware(datetime(
            int(2023),int(2),int(1)),tz)
        # past date = 1 Feb 2022
        past_date = make_aware(datetime(
            int(2022),int(2),int(1)),tz)
        #
        ref_date = now
        #print(ref_date) 
        #
        active_workers = self.filter(Q(is_active=True, 
                                    starting_at__lte=ref_date,
                                    ending_at__isnull=True) |
                                    Q(is_active=True, 
                                    starting_at__lte=ref_date,
                                    ending_at__gte=ref_date)).values_list("name","company","description","starting_at","ending_at")
        return active_workers

    def get_supervisor_company(self, obj):
        get_supervisor_company = self.filter(id=obj.employee.id).values_list('company')   
        return get_supervisor_company 
   

class WorkerSupervisorQuerySet(models.QuerySet):
    #    
    # Zie https://spookylukey.github.io/django-views-the-right-way/thin-views.html
   
    def get_supervisor(self, obj):
        get_supervisor = self.filter(worker=obj.id).values_list('supervisor__employee__name')        
        return get_supervisor   

    def get_supervised_team(self, obj):
        get_supervised_team = self.filter(supervisor=obj.id).values_list('worker__name')             
        return get_supervised_team        
    

# OrgUnit, Employee, Organisation
class OrgUnit(models.Model):
    # CHOICES
    HIERARCHICAL = 'HI'
    FUNCTIONAL = 'FU'
    TYPE_ORG_UNIT = (
        (HIERARCHICAL, 'Hierarchical Unit'),
        (FUNCTIONAL, 'Functional Unit'),       
    )

    # DATABASE FIELDS
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name=('parent'),
        related_name='children',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=2,choices=TYPE_ORG_UNIT, db_index=True)
    is_active = models.BooleanField(default=True)    
    starting_at = models.DateField(default=date.today, null=True, blank=True)    
    ending_at = models.DateField(null=True, blank=True)

    # META CLASS
    class Meta:
        verbose_name = 'org_unit'
        verbose_name_plural = 'org_units'

    def __str__(self):
        return self.name
    
    objects = OrgUnitQuerySet.as_manager()
    

         
class Worker(models.Model):
    # DATABASE FIELDS
    # CHOICES
    KYNDRYL_BE = 'KYND-BE'
    KYNDRYL_CIC_PL = 'CIC-PL'
    PI_SQUARE = 'PISQ-BE'
    COMPANY_CODE = (
        (KYNDRYL_BE, 'Kyndryl BE'),
        (PI_SQUARE, 'PI-SQUARE'),       
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.CharField(max_length=7,choices=COMPANY_CODE, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)    
    is_active = models.BooleanField(default=True)    
    starting_at = models.DateField(default=date.today, null=True, blank=True)    
    ending_at = models.DateField(null=True, blank=True)

    # META CLASS
    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'

    def __str__(self):
        return self.name

    objects = WorkerQuerySet.as_manager()
   
class Supervisor(models.Model):
    # 
    employee = models.ForeignKey(
        'Worker',
        on_delete=models.CASCADE,
        verbose_name=('employee'),
        related_name='supervisor',
        blank=True,
        null=True,
    )

    supervising_group = models.ManyToManyField(Worker, through='WorkerSupervisor',related_name='worker',)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    description = models.TextField(null=True, blank=True)    
    is_active = models.BooleanField(default=True)    
    starting_at = models.DateField(default=date.today, null=True, blank=True)    
    ending_at = models.DateField(null=True, blank=True)

    # META CLASS
    class Meta:
        verbose_name = 'supervisor'
        verbose_name_plural = 'supervisors'

    def __str__(self):
        return self.employee.name

class WorkerSupervisor(models.Model):
    # CHOICES
    HIERARCHICAL = 'HI'
    FUNCTIONAL = 'FU'
    TYPE_SUPERVISOR_ROLE = (
        (HIERARCHICAL, 'Hierarchical Manager'),
        (FUNCTIONAL, 'Functional Manager'),       
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    type = models.CharField(max_length=2,choices=TYPE_SUPERVISOR_ROLE, db_index=True)
    is_active = models.BooleanField(default=True)    
    starting_at = models.DateField(default=date.today, null=True, blank=True)    
    ending_at = models.DateField(null=True, blank=True)


    objects = WorkerSupervisorQuerySet.as_manager()
    