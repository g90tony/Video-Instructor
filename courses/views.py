from django.contrib.auth.models import User
from django.http import response
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response 

from .models import Category, Course, Lesson, Profile, Progress, RegisteredCourses
from .serializers import CourseSerializer, LessonSerializer,ProfileSerializer,ProgressSerializer,RegisterCourseSerializer, ListProfileSerializer, ListCategorySerializer, ListProgressSerializer, ListRegisterCourseSerializer

# Create your views here.
@login_required(login_url='/accounts/login')
def index(request):
    
    current_user = request.user
    title = 'Video Instructor: Dashboard'
    
    user_profile = Profile.objects.filter(user = current_user).first()
    
    if user_profile is  None:
        return redirect('/profile/create')
    
    registered_courses = RegisteredCourses.objects.filter(profile = user_profile).all()
    
    new_courses = Course.objects.order_by('-created')[:10]
    
    return render(request, 'dashboard.html', {'title':title, 'current_user':current_user, 'registered':registered_courses, 'recent':new_courses })

@login_required(login_url='/accounts/login')
def browse_registered(request):
    
    current_user = request.user
    user_profile = Profile.objects.filter(user=current_user).first()
    title = 'Browse Courses: Video Instructor'
    registered_courses = RegisteredCourses.objects.filter(profile= user_profile).all()
    
    return render(request, 'register_courses.html', {'title': title, 'registered': registered_courses} )

@login_required(login_url='/accounts/login')
def view_registered(request, lesson_id):
    
    current_user = request.user
    user_profile = Profile.objects.filter(user = current_user).first()
    title = 'Learn: Video Instructor'
    current_lesson = Lesson.objects.filter(id = lesson_id).first()
    registered_lessons = Lesson.objects.filter(course = current_lesson.course).all()
    
    count = 0
    end = False
    next_lesson_obj = ''
    while end == False :
        for lesson in registered_lessons:
            if lesson == current_lesson:
                next_lesson = count + 1
                next_lesson_obj = registered_lessons[next_lesson].lesson
                end = True
                
        count = count + 1
        
    if next_lesson_obj == None:
        next_lesson_obj = '/'

        
    return render(request, 'register_courses_view.html', {'title':title, 'current_lesson': current_lesson, 'next_lesson': next_lesson_obj,'lessons': registered_lessons,})

@login_required(login_url='/accounts/login')
def browse_courses(request):
    
    current_user = request.user
    title = 'Browse Courses: Video Instructor'
    courses = Course.objects.all()

    return render(request, 'browse_courses.html', {'title': title, 'courses': courses} )

@login_required(login_url='/accounts/login')
def view_course(request, course_id):
    title = 'View Course: Video Instructor'
    current_user = request.user
    
    course = Course.objects.filter(id=course_id).first()
    
    
    return render(request, 'browse_courses_view.html', {'title': title, 'course': course} )

@login_required(login_url='/accounts/login')
def register_course(request, course_id):
    
    course = Course.objects.filter(id=course_id).first()
    
    current_user = request.user
    
    user_profile = Profile.objects.filter(user=current_user).first() 
    
    new_registration = RegisteredCourses(profile=user_profile, course=course)
    
    new_registration.save()
    
    return redirect('/')
    

@login_required(login_url='/accounts/login')
def edit_profile(request):
    
    title = 'Edit Profile; Video Instructor'
    current_user = request.user
    
    user_profile = Profile.objects.filter(user=current_user).first()
    
    return render(request, 'edit_profile.html',{ 'title': title, "current_user": user_profile })


@login_required(login_url='/accounts/login/')
def search_courses(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        
        results = Course.objects.filter(name= search_query).all()
        title = 'Search Results: Video Instructor'
        
        if results:
            return render(request, 'search_results.html', {'title': title, 'results': results})
        else:
            return render(request, 'search_results.html', {'title': title, 'message':f'There was were no results for {search_query}'})
    
    else: 
        return redirect('/courses/browse')


@login_required(login_url='/accounts/login/')
def search_registered(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        
        results = Course.objects.filter(name= search_query).all()
        title = 'Search Results: Video Instructor'
        if results:
            return render(request, 'search_results.html', {'title': title, 'results': results})
        else:
            return render(request, 'search_results.html', {'title': title, 'message':f'There was were no results for {search_query}'})
                      
                      
@login_required(login_url='accounts/login/')
def update_email(request):
    if request.method == 'POST':
        
        current_user = request.user
        user_obj = User.objects.filter(user=current_user).first()
        
        updated_email = request.POST.get('new_email')
        if updated_email:
            user_obj.email = update_email
            
            user_obj.save()


@login_required(login_url='accounts/login/')
def update_avatar(request):
    if request.method == 'POST':
        
        current_user = request.user
        user_obj = User.objects.filter(user=current_user).first()
        
        updated_avatar = request.FILES['new_avatar']
        
        user_obj.avatar = updated_avatar
        
        user_obj.save()


@login_required(login_url='accounts/login/')
def create_profile(request):
    current_user = request.user
    title = 'Create Profile: Video Instructor'
        
        
    if request.method == 'POST':
        
        updated_avatar = request.FILES['new_avatar']
        updated_first_name = request.POST.get('first_name')
        updated_last_name = request.POST.get('last_name')
        
        new_profile = Profile(avatar=updated_avatar, first_name=updated_first_name, last_name=updated_last_name, user=current_user)
        
        new_profile.save()
        
        return redirect('/')
    
    else:
        return render(request, 'create_profile.html', {'title': title})
    
# @login_required(login_url='/accounts/login/')
# def load_next_lesson(request):
#     if request.method == 'POST':
        
         
        
    

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
        
    