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


class ObjDetails(models.Model):

    EXE = 'Execution'
    EDU = 'Education'
    TEMP = 'Template'
    DOMAIN = (
        (EXE, 'Execution'),
        (EDU, 'Education'),
        (TEMP, 'Template'),
    )

    employee = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        verbose_name=('employee'),
        related_name='objDetails_employee',
        blank=True,
        null=True,
    )
    # Wie heeft de record aangemaakt. Oorspronkelijke owner is de accout
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,)
    # Wie is de owner, in praktijk de TL, de owner gaat samen met de employee aanpassingen kunnen maken
    owner = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        verbose_name=('owner'),
        related_name='objDetails_owner',
        blank=True,
        null=True,
    )

    domain = models.CharField(
        max_length=10, choices=DOMAIN, default="Execution")
    subject = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    # META CLASS

    def __str__(self):
        return self.employee.name

    # MANAGER
    objects = ObjectiveQuerySet.as_manager()

class ObjDetailsResult(models.Model):

    # CHOICES
    UNSAT = 'UNSAT'
    BELOW = 'BELOW'
    JOB = 'JOB'
    ABOVE = 'ABOVE'
    EXCEP = 'EXCEP'
    SCORES = (
        (UNSAT, 'Unsat'),
        (BELOW, 'Below Joblevel'),
        (JOB, 'Joblevel'),
        (ABOVE, 'Above Joblevel'),
        (EXCEP, 'Exceptional'),
    )

    objective = models.ForeignKey(
        ObjDetails,
        on_delete=models.CASCADE,
        verbose_name=('objective_result'),
        related_name='objDetailsResult',
        blank=True,
        null=True,
    )

    # Wie heeft de record aangemaakt. Oorspronkelijke owner is de account
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,)

    comment_result_set = models.TextField(null=True, blank=True)
    comment_result_approval = models.TextField(null=True, blank=True)
    objectives_approval_at = models.DateField(null=True, blank=True)

    calibration_result_midyear = models.CharField(
        max_length=10, choices=SCORES)
    midyear_at = models.DateField(null=True, blank=True)
    score_result_midyear = models.CharField(max_length=10, choices=SCORES)
    comment_result_midyear = models.TextField(null=True, blank=True)

    calibration_result_endyear = models.CharField(
        max_length=10, choices=SCORES)
    endyear_at = models.DateField(null=True, blank=True)
    score_result_endyear = models.CharField(max_length=10, choices=SCORES)
    comment_result_endyear = models.TextField(null=True, blank=True)
    endyear_approval_at = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # META CLASS

    def __str__(self):
        return self.objective.employee.name

    # MANAGER
    objects = ObjectiveQuerySet.as_manager()

class ObjMaster(models.Model):
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

    Y2020 = '2020'
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

    # Aan wie zal deze record worden aangewezen
    employee = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        verbose_name=('employee'),
        related_name='objMaster_employee',
        blank=True,
        null=True,
    )

    # Wie heeft de record aangemaakt. Oorspronkelijke owner is de accout
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,)
    
    # Wie is de owner, in praktijk de TL, de owner gaat samen met de employee aanpassingen kunnen maken
    owner = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        verbose_name=('owner'),
        related_name='objMaster_owner',
        blank=True,
        null=True,
    )

    # Welke ObjDetails zijn er gekoppeld aan deze master 
    # 
    obj_details = models.ForeignKey(
        ObjDetails,
        on_delete=models.CASCADE,
        verbose_name=('obj_details'),
        related_name='objMaster',
        blank=True,
        null=True,
    )

    ref_period = models.CharField(
        max_length=5, choices=REF_PERIOD, db_index=True)
    stage = models.CharField(max_length=15, choices=STAGES, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # META CLASS

    def __str__(self):
        return self.employee.name

    # MANAGER
    objects = ObjectiveQuerySet.as_manager()



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

    EXE = 'Execution'
    EDU = 'Education'
    TEMP = 'Template'       
    DOMAIN = (
        (EXE, 'Execution'),
        (EDU, 'Education'),           
        (TEMP, 'Template'),                 
    )


    employee = models.ForeignKey(
            Worker,
            on_delete=models.CASCADE,
            verbose_name=('employee'),
            related_name='objectives',
            blank=True,
            null=True,
        )
    # Wie heeft de record aangemaakt. Oorspronkelijke owner is de accout
    creator = models.ForeignKey(
              settings.AUTH_USER_MODEL,
              on_delete=models.CASCADE,
              blank=True,
              null=True,)
    # Wie is de owner, in praktijk de TL, de owner gaat samen met de employee aanpassingen kunnen maken
    owner = models.ForeignKey(
            Worker,
            on_delete=models.CASCADE,
            verbose_name=('owner'),
            related_name='objective_owner',
            blank=True,
            null=True,
        )
        
    ref_period = models.CharField(max_length=5,choices=REF_PERIOD, db_index=True)
    stage  = models.CharField(max_length=15,choices=STAGES, db_index=True)
    domain  = models.CharField(max_length=10,choices=DOMAIN,default="Execution")
    subject = models.CharField(max_length=128,blank=True, null=True)
    description = models.TextField(null=True, blank=True) 
     

    # META CLASS

    def __str__(self):
            return self.employee.name

    # MANAGER 
    objects = ObjectiveQuerySet.as_manager()

class ObjectiveResult(models.Model):
    # CHOICES
    UNSAT = 'UNSAT'
    BELOW = 'BELOW'
    JOB = 'JOB'
    ABOVE = 'ABOVE'
    EXCEP = 'EXCEP'
    SCORES = (
        (UNSAT, 'Unsat'),
        (BELOW, 'Below Joblevel'),
        (JOB, 'Joblevel'),
        (ABOVE, 'Above Joblevel'),
        (EXCEP, 'Exceptional'),                    
    )   

    objective = models.ForeignKey(
            Objective,
            on_delete=models.CASCADE,
            verbose_name=('objective_result'),
            related_name='objective',
            blank=True,
            null=True,
        )

    comment_result_set = models.TextField(null=True, blank=True) 
    comment_result_approval = models.TextField(null=True, blank=True)
    calibration_result_midyear =  models.CharField(max_length=10,choices=SCORES)
    score_result_midyear =  models.CharField(max_length=10,choices=SCORES)
    comment_result_midyear = models.TextField(null=True, blank=True) 
    calibration_result_endyear =  models.CharField(max_length=10,choices=SCORES)
    score_result_endyear =  models.CharField(max_length=10,choices=SCORES)
    comment_result_endyear = models.TextField(null=True, blank=True)
   
    #
    setobjectives_at = models.DateField(null=True, blank=True)
    objectives_approval_at = models.DateField(null=True, blank=True)
    midyear_at = models.DateField(null=True, blank=True)
    endyear_at = models.DateField(null=True, blank=True)
    endyear_approval_at = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    # META CLASS

    def __str__(self):
            return self.objective.employee.name

    # MANAGER 
    #objects = ObjectiveQuerySet.as_manager()
    