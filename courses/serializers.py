from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers

from .models import Category, Course, Lesson, Profile, Progress, RegisteredCourses

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","email",)
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")
        
class CourseSerializer(serializers.ModelSerializer):
    
    thumbnail = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ("id", "name", "description", "category", "thumbnail",) 
        
    def get_thumbnail(self, course):
        request = self.context.get('request')
        thumbnail = course.thumbnail.url
        
        return request.build_absolute_uri(thumbnail)
    
    
class LessonSerializer(serializers.ModelSerializer):
    
    course = CourseSerializer(many=False)
    
    class Meta:
        model = Lesson
        fields = ("id", "title", "descripion", "lesson", "course",) 
        
        
class ProfileSerializer(serializers.ModelSerializer):
    
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ("id", "avatar", "first_name", "last_name",) 
        
    def get_avatar(self, profile):
        request = self.context.get('request')
        avatar = profile.avatar.url
        
        return request.build_absolute_uri(avatar)
    
    
class ProgressSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many = False)
    course = CourseSerializer(many = False)
    lesson = LessonSerializer(many = False)
    
    class Meta:
        model = Progress
        fields = ("id", "profile", "course", "lesson",) 
        
        
class RegisterCourseSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer(many = False)
    course = CourseSerializer(many = False)
            
    class Meta:
        model: RegisteredCourses
        fields = ("id", "profile", "course",) 
        
        
# List Models Serializers
class ListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name")
        
class ListCourseSerializer(serializers.ModelSerializer):
    
    thumbnail = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ("name", "description", "category", "thumbnail",) 
        
    def get_thumbnail(self, course):
        request = self.context.get('request')
        thumbnail = course.thumbnail.url
        
        return request.build_absolute_uri(thumbnail)
    
    
class ListLessonSerializer(serializers.ModelSerializer):
    
    course = CourseSerializer(many = False)
    
    class Meta:
        model = Lesson
        fields = ("title", "descripion", "lesson", "course",) 
        
        
class ListProfileSerializer(serializers.ModelSerializer):
    
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ("avatar", "first_name", "last_name",) 
        
    def get_avatar(self, profile):
        request = self.context.get('request')
        avatar = profile.avatar.url
        
        return request.build_absolute_uri(avatar)
    
    
class ListProgressSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many = False)
    course = CourseSerializer(many = False)
    lesson = LessonSerializer(many = False)
    
    class Meta:
        model = Progress
        fields = ("profile", "course", "lesson",) 
        
        
class ListRegisterCourseSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer(many = False)
    course = CourseSerializer(many = False)
            
    class Meta:
        model: RegisteredCourses
        fields = ("profile", "course",) 