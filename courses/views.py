from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView

from .models import Category, Course, Lesson, Profile, Progress, RegisteredCourses

# Create your views here.
@login_required(login_url='/accounts/login')
def index(request):
    pass


