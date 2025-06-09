from django.shortcuts import render
from .models import Subject, Student, Score

def index(request):
    students = Student.objects.all()
    data = {
        'subjects': Subject.objects.all(),
        'students' : students,
        'scores' : Score.objects.all()
    }
    return render(request, 'index.html', data)


