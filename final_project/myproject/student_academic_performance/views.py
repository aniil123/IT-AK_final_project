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

def add_student(request):
    print(request.POST)
    score_forms = []
    if request.method == 'POST':
        student_form = AddStudentForm(request.POST, prefix='student')
        form_valid = True
        for subject in Subject.objects.all():
            score_form = AddScoreForm(request.POST, prefix=subject.name)
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
        student_form = AddStudentForm(prefix='student')
        for subject in Subject.objects.all():
            score_form = AddScoreForm(prefix=subject.name)
            score_form.fields['value'].label = subject.name
            score_forms.append(score_form)
    return render(request, 'student_academic_performance/add_student.html', {'student_form': student_form, 'score_forms': score_forms})

def add_subject(request):
    score_forms = []
    if request.method == 'POST':
        subject_form = AddSubjectForm(request.POST, prefix='subject')
        form_valid = True
        for student in Student.objects.all():
            score_form = AddScoreForm(request.POST, prefix=f'student{student.id}')
            if not score_form.is_valid():
                form_valid = False
            score_forms.append(score_form)
        if subject_form.is_valid() and form_valid:
            new_subject = Subject.objects.create(name=subject_form.cleaned_data.get("name"))
            students = Student.objects.all()
            for i in range(len(students)):
                print(score_forms[i].fields)
                Score.objects.create(
                    student=students[i], 
                    subject=new_subject,
                    value=score_forms[i].cleaned_data.get('value')
                    )
            return redirect('viewing')
    else:
        subject_form = AddSubjectForm(prefix='subject')
        for student in Student.objects.all():
            score_form = AddScoreForm(prefix=f'student{student.id}')
            score_form.fields['value'].label = f'Студент id={student.id}, имя={student.name}, фамилия={student.surname}'
            score_forms.append(score_form)
    return render(request, 'student_academic_performance/add_subject.html', {'subject_form': subject_form, 'score_forms': score_forms})

def delete_student(request):
    if request.method == 'POST':
        form = SelectStudentForm(request.POST)
        form.fields['id'].label = 'Id студента, которого нужно удалить'
        if form.is_valid():
            try:
                wanted_student = Student.objects.get(id=form.cleaned_data.get('id'))
                Score.objects.filter(student__id__contains=form.cleaned_data.get('id')).delete()
                wanted_student.delete()
                return redirect('viewing')
            except:
                print("can't delete student")
    else:
        form = SelectStudentForm()
        form.fields['id'].label = 'Id студента, которого нужно удалить'
    return render(request, 'student_academic_performance/delete_student.html', {'form': form})

def delete_subject(request):
    if request.method == 'POST':
        form = SelectSubjectForm(request.POST)
        form.fields['name'].label = 'Название предмета, который нужно удалить'
        if form.is_valid():
            try:
                wanted_subject = Subject.objects.get(name=form.cleaned_data.get('name'))
                Score.objects.filter(subject__name__contains=form.cleaned_data.get('name')).delete()
                wanted_subject.delete()
                return redirect('viewing')
            except:
                print("can't delete subject")
    else:
        form = SelectSubjectForm()
        form.fields['name'].label = 'Название предмета, который нужно удалить'
    return render(request, 'student_academic_performance/delete_subject.html', {'form': form})
