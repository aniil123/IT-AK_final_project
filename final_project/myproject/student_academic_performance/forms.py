from django import forms
from django.core.exceptions import ValidationError
from .models import *

class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'email']

class AddScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['value']
        widgets = {
            'value': forms.Select(choices=[
                (2, 2),
                (3, 3),
                (4, 4),
                (5, 5)
            ], attrs={'class': 'form-control'})
        }

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
    
class SelectStudentForm(forms.Form):
    id = forms.CharField(max_length=4)

class SelectSubjectForm(forms.Form):
    name = forms.CharField(max_length=20)
    