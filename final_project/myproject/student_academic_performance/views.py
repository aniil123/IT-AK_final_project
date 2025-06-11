from django.shortcuts import render, redirect
from .models import Subject, Student, Score
from collections import defaultdict
from .forms import *

def index(request):
    subjects = Subject.objects.all()
    student_statistics = defaultdict(dict)
    students_average_grade = defaultdict(int)
    subjects_average_grade = defaultdict(int)
    for score in Score.objects.all():
        student = score.student
        subject = score.subject
        student_statistics[student][subject] = score.value
        students_average_grade[student] += score.value
        subjects_average_grade[subject] += score.value

    subjects_count = len(Subject.objects.all())
    students_average_grade = [students_average_grade[student] / subjects_count for student in students_average_grade.keys()]
    students_count = len(Student.objects.all())
    subjects_average_grade = [subjects_average_grade[subject] / students_count for subject in subjects_average_grade.keys()]

    students_data = []
    students_average_grade_iter = iter(students_average_grade)
    for student, subjects_scores in student_statistics.items():
        students_data.append([student, subjects_scores.values(), next(students_average_grade_iter)])
    context = {
        'subjects': subjects,
        'subjects_average_grade': subjects_average_grade,
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

def add_student(request):
    print(request.POST)
    score_forms = []
    if request.method == 'POST':
        student_form = AddStudentForm(request.POST)
        form_valid = True
        for subject in Subject.objects.all():
            score_form = AddScoreForm(request.POST)
            if not score_form.is_valid():
                form_valid = False
            score_forms.append(score_form)
        if student_form.is_valid() and form_valid:
            new_student = Student.objects.create(
                name=student_form.cleaned_data.get('name'), 
                surname=student_form.cleaned_data.get('surname'),
                email=student_form.cleaned_data.get('email')
            )
            subjects = Subject.objects.all()
            for i in range(len(subjects)):
                Score.objects.create(
                    student=new_student,
                    subject=subjects[i],
                    value=score_forms[i].cleaned_data.get('value')
                )
            return redirect('viewing')
    else:
        student_form = AddStudentForm()
        for subject in Subject.objects.all():
            score_form = AddScoreForm()
            score_form.fields['value'].label = subject.name
            score_forms.append(score_form)
    return render(request, 'student_academic_performance/add_student.html', {'student_form': student_form, 'score_forms': score_forms})

