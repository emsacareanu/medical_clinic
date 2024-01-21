# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Employee

class EmployeeForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('medic', 'Medic'),
        ('guard', 'Guard'),
        ('nurse', 'Nurse'),
        ('administrator', 'Administrator'),
        ('janitor', 'Janitor'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = Employee
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

   
        non_null_fields = ['employee_ID', 'DOB', 'phone_no', 'e_name', 'e_surname', 'role', 'DOE']
        for field in non_null_fields:
            if cleaned_data.get(field) is None:
                raise ValidationError(f"{field} cannot be empty.")


        max_length_fields = {'employee_ID': 6, 'CNP': 13, 'phone_no': 10, 'e_name': 50, 'e_surname': 50}
        for field, max_length in max_length_fields.items():
            value = cleaned_data.get(field)
            if value and len(value) > max_length:
                raise ValidationError(f"{field} must be at most {max_length} characters long.")

        return cleaned_data
