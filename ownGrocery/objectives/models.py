from django.db import models

from datetime import date, datetime
from django.utils import timezone
from django.utils.timezone import get_current_timezone, make_aware, now
from django.db.models import Q
from django.conf import settings
from teams.models import Worker


# Create your models here.

class ObjectiveQuerySet(models.QuerySet):

    def no_of_objectives(self, obj):
        return self.filter(parent=obj).count()

    def get_employee(self, obj):
        print(self)
        print(obj)
        return self.employee__name

    
class Objective(models.Model):
    # CHOICES
    START = 'START'
    SET = 'SET-OBJ'
    RUN = 'RUN-OBJ'
    CALIB_MIDYEAR = 'CALIB-MIDYEAR'
    MIDYEAR = 'MIDYEAR'
    CALIB_ENDYEAR = 'CALIB-ENDYEAR'
    ENDYEAR = 'ENDYEAR'
    CLOSE = 'CLOSE-OBJ'
    STAGES = (
        (START, 'Start Objectives'),
        (SET, 'Set Objectives'),
        (RUN, 'Execute Objectives'),
        (CALIB_MIDYEAR, 'Calibration for MidYear'),
        (MIDYEAR, 'MidYear'),  
        (CALIB_ENDYEAR, 'Calibration for MidYear'),
        (ENDYEAR, 'EndYear'), 
        (CLOSE, 'Close'),           
    )

    Y2020 =  '2020'
    Y2021 = '2021'
    Y2022 = '2022'
    Y2023 = '2023'
    Y2024 = '2024'
    Y2025 = '2025'       
    REF_PERIOD = (
        (Y2020, '2020'),
        (Y2021, '2021'),
        (Y2022, '2022'),
        (Y2023, '2023'),
        (Y2024, '2024'),
        (Y2025, '2025'),             
    )


    employee = models.ForeignKey(
            Worker,
            on_delete=models.CASCADE,
            verbose_name=('employee'),
            related_name='objectives',
            blank=True,
            null=True,
        )
    ref_period = models.CharField(max_length=5,choices=REF_PERIOD, db_index=True)
    stage  = models.CharField(max_length=15,choices=STAGES, db_index=True)
    description = models.TextField(null=True, blank=True) 
    #score = models.JSONField(default=dict, null=False)
    score = models.TextField(null=True, blank=True)
    setobjectives_at = models.DateField(null=True, blank=True)
    objectives_approval_at = models.DateField(null=True, blank=True)
    midyear_at = models.DateField(null=True, blank=True)
    endyear_at = models.DateField(null=True, blank=True)
    endyear_approval_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    # META CLASS

    def __str__(self):
            return self.employee.name

    # MANAGER 
    objects = ObjectiveQuerySet.as_manager()