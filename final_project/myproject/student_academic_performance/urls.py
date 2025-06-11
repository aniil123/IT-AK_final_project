from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='viewing'),
    path('editing/', editing, name='editing'),
    path('add_student/', add_student, name='add_student')
]