from django.contrib.auth.models import AbstractUser
from django.db import models

class AppointmentsModel(AbstractUser):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField(default=0)

class Employee(models.Model):
    employee_ID = models.CharField(max_length=6, primary_key=True)
    CNP = models.CharField(max_length=13, null=True, blank=True)
    DOB = models.DateTimeField(null=True, blank=True)
    phone_no = models.CharField(max_length=10, null=True, blank=True)
    e_name = models.CharField(max_length=50, null=True, blank=True)
    e_surname = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=20, null=True, blank=True, choices=[('medic', 'Medic'), ('guard', 'Guard'), ('nurse', 'Nurse'), ('administrator', 'Administrator'), ('janitor', 'Janitor')])
    DOE = models.DateTimeField(null=True, blank=True)
