from django.shortcuts import render
from .models import Subject, Student, Score
from collections import defaultdict

def index(request):
    subjects = Subject.objects.all()
    student_statistics = defaultdict(dict)
    for score in Score.objects.all():
        student = score.student
        subject_name = score.subject.name
        student_statistics[student][subject_name] = score.value
    students_data = []
    for student, subjects_scores in student_statistics.items():
        students_data.append([student, subjects_scores.values()])
    context = {
        'subjects': subjects,
        'students_data': students_data,
    }
    return render(request, 'student_academic_performance/index.html', context=context)

def editing(request):
    subjects = Subject.objects.all()
    student_statistics = defaultdict(dict)
    for score in Score.objects.all():
        student = score.student
        subject_name = score.subject.name
        student_statistics[student][subject_name] = score.value
    students_data = []
    for student, subjects_scores in student_statistics.items():
        students_data.append([student, subjects_scores.values()])
    context = {
        'subjects': subjects,
        'students_data': students_data,
    }
    return render(request, 'student_academic_performance/editing.html', context=context)

