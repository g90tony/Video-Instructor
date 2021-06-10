from django.contrib.auth.models import User
from django.http import response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response 

from .models import Category, Course, Lesson, Profile, Progress, RegisteredCourses
from .serializers import CategorySerializer,CourseSerializer, LessonSerializer,ProfileSerializer,ProgressSerializer,RegisterCourseSerializer, ListProfileSerializer, ListCategorySerializer, ListCourseSerializer, ListLessonSerializer, ListProgressSerializer, ListRegisterCourseSerializer

# Create your views here.
@login_required(login_url='/accounts/login')
def index(request):
    pass

# ===========================================================================================================================================================================================================================================================================================================
# API Routes
# ===========================================================================================================================================================================================================================================================================================================
    
#////////////////////////////////////////////////////////////////////////////////////////////////////// 
# API Routes
# Name: ListCategory
# Endpoint: api/categories/
# Desc: handles all category creation requests
# Methods: GET        
class ListCategory(APIView):
    
    @api_view(http_method_names=['GET'])
    def get_all(self, request, format = None):
        
        all_categories = Category.objects.all()
        
        serializers = ListCategorySerializer(all_categories, context = {'request': request}, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
   
    
#///////////////////////////////////////////////////////////////////////////////////////////////////// 
# API Routes
# Name: SingleCourse
# Endpoint: api/courses/<course_id>
# Desc: handles all single course requests
# Methods: GET        
class SingleCourse(APIView):
    
    def get_course_obj(pk):
        return Course.objects.get(id=pk)
    
    @api_view(http_method_names=['GET'])
    def get_course(self, request, course_id, format=None):
        
        course_obj = self.get_course(course_id)
        
        serializers = CourseSerializer(course_obj, context = {'request': request}, many = True)
        return Response(serializers.data, status=status.HTTP_200_OK) 
        
    
    
#////////////////////////////////////////////////////////////////////////////////////////////////////// 
# API Routes
# Name: ListCourse
# Endpoint: api/courses/
# Desc: handles all bulk courses requests
# Methods: GET, POST        
class ListCourses(APIView):
    
    @api_view(http_method_names=['GET'])
    def get_all_courses(self, request, format=None ):
        
        all_courses = Course.objects.all()
        
        serializers = ListCourses(all_courses, context={'request': request}, many=True)
        
        Response(serializers.data, status=status.HTTP_200_OK)
        
    
    
#////////////////////////////////////////////////////////////////////////////////////////////////////// 
# API Routes
# Name: SearchCourses
# Endpoint: api/courses/search/<search_query>
# Desc: handles all bulk courses requests
# Methods: GET, POST        
class SearchCourses(APIView):
    
    @api_view(http_method_names=['GET'])
    def get_all_courses(self, request, search_query, format=None ):
        
        all_courses = Course.objects.filter(title=search_query).all()
        
        serializers = ListCourses(all_courses, context={'request': request}, many=True)
        
        Response(serializers.data, status=status.HTTP_200_OK)
        
    
     
    
#////////////////////////////////////////////////////////////////////////////////////////////////////// 
# API Routes
# Name: ListLessons
# Endpoint: api/lesson/<course_id>
# Desc: handles all bulk lessons requests
# Methods: GET, POST        
class ListLessons(APIView):
    
    def get_course_object(pk):    
        return Course.objects.get(id=pk)
    
    @api_view(http_method_names=['GET'])
    def get_course_lessons(self, request, course_id, format=None):
        
        course_obj = self.get_course_object(course_id)
        
        course_lessons = Lesson.objects.filter(course=course_obj).all()
        serializers = LessonSerializer(course_lessons, context={'request': request}, many=True)
        
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    
   
# /////////////////////////////////////////////////
# Name: SingleProfile
# Endpoint: api/profile/<profile_id>
# Desc: handles all requests for a single profile
# Methods: GET
class SingleProfile(APIView):
    
    def get_profile_object(pk):
        return Profile.objects.get(id=pk)    

    def get_course_object(pk):
        return Course.objects.get(id=pk)    
    
    @api_view(http_method_names=['GET'])
    def load_profile(self, request, profile_id, format=None):
        profile_obj = self.get_profile_object(profile_id)
        
        serializers = ProfileSerializer(profile_obj, context = {"request": request}, many = False)
        return Response(serializers.data, status= status.HTTP_200_OK)  
    
    
    
# /////////////////////////////////////////////////
# Name: ListProfile
# Endpoint: api/profile/
# Desc: handles all requests for a single profile
# Methods:POST
class ListProfile(APIView):
    
    def get_user_obj(pk):
        
        return User.objects.get(id=pk)
    
    @api_view(http_method_names=['POST'])
    def create_profile(self, request, format = None):
        
        serializers = ListProfileSerializer(data=request.data, context= ({'request': request}), many= False)
        
        if serializers.is_valid():
            Response(status=status.HTTP_201_CREATED)
            
        else: 
            Response(status=status.HTTP_400_BAD_REQUEST)
        
        
#///////////////////////////////////////////////////////////////////////////////////////////////////// 
# API Routes
# Name: SingleProgress
# Endpoint: api/progress/<progress_id>
# Desc: handles all single progress requests
# Methods: GET, POST        
class SingleProgress(APIView):
    
    def get_progress_obj(pk):
        return Progress.objects.get(id=pk)
    
    @api_view(http_method_names=['GET'])
    def get_progress(self, request, progress_id, format):
        
        progress_obj = self.get_progress(progress_id)
        
        serializers = ProgressSerializer(progress_obj, context={'request': request}, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    
#////////////////////////////////////////////////////////////////////////////////////////////////////// 
# API Routes
# Name: ListProgress
# Endpoint: api/progress/<course_id>+<profile_id>
# Desc: handles all bulk progress requests
# Methods: GET, POST        
class ListProgress(APIView):
    
    def get_course_obj(pk):
        return Course.objects.get(id=pk)

    def get_profile_obj(pk):
        return Profile.objects.get(id=pk)
    
    @api_view(http_method_names=['GET'])
    def get_course_progress(self, request, course_id, profile_id, format=None):
        
        course_obj = self.get_course_obj(course_id)
        profile_obj = self.get_profile_obj(profile_id)
        
        course_progress = Progress.objects.filter(profile=profile_obj, course=course_obj)
        
        serializers = ListProgressSerializer(course_progress, many=True)
        
        return Response(serializers.data, status=status.HTTP_200_OK)
    


    
#////////////////////////////////////////////////////////////////////////////////////////////////////// 
# API Routes
# Name: ListRegisterCourse
# Endpoint: api/courses/registered
# Desc: handles all bulk registed courses requests
# Methods: GET, POST
class ListRegisterCourse(APIView):
       
    def get_profile_obj(pk):
        return Profile.objects.get(id = pk)
    
    @api_view(http_method_names=['GET'])
    def get_registered(self, request, profile_id, format = None):
        
        profile_obj = self.get_profile_obj(profile_id)
        
        registered_courses = RegisteredCourses.objects.filter(profile = profile_obj).all()
        
        serializers = RegisterCourseSerializer(registered_courses, context = {'request': request}, many = True)

        return Response(serializers.data, status= status.HTTP_200_OK)
    
    
    @api_view(http_method_names=['POST'])
    def register_course(self, request, format = None):
        
        serializers = ListRegisterCourseSerializer(data=request.data)

        if serializers.is_valid():
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST )
        
    