from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='viewing'),
    path('add_student/', add_student, name='add_student'),
    path('add_subject/', add_subject, name='add_subject'),
    path('delete_subject/', delete_subject, name='delete_subject'),
    path('delete_student/', delete_student, name='delete_student')
]