from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=200, null=False)
    surname = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False, unique=True)

    @property
    def fio(self):
        return f'{self.name} {self.surname}'

    def __repr__(self):
        return f'Student(name="{self.name}", surname="{self.surname}", email="{self.email}")'
    

class Subject(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Subject(name="{self.name}")'


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f'{self.student.fio}: {self.subject} -> {self.value:.2f}'

    def __repr__(self):
        return f'Student(student="{self.student}", subject="{self.subject}", value="{self.value}")'