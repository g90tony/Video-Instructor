"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.urls.conf import include

from . import views as API_ROUTES

urlpatterns = [
    path('', view=API_ROUTES.index, name='Home'),
    
    path('courses/registered', view=API_ROUTES.browse_registered, name='Browse Registered'),
    path('course/registered/search', view=API_ROUTES.search_registered, name='Search Registered'),
    path('courses/registered/view/<int:lesson_id>', view=API_ROUTES.view_registered, name='View Registered'),
    path('courses/registered/register/<int:course_id>', view=API_ROUTES.register_course, name='View Registered'),
    
    path('courses/browse', view=API_ROUTES.browse_courses, name='Browse Course'),
    path('course/browse/search', view=API_ROUTES.search_courses, name='Search Courses'),
    path('courses/browse/view/<int:course_id>', view=API_ROUTES.view_course, name='View Course'),
    
    path('profile/create/', view=API_ROUTES.create_profile, name='Create Profile'),
    path('profile/edit/', view=API_ROUTES.edit_profile, name='Edit Profile'),
    path('profile/update/email', view=API_ROUTES.edit_profile, name='Update Email'),
    path('profile/update/avatar', view=API_ROUTES.edit_profile, name='Update Avatar'),
    
    
    
    path('api/categories/', view=API_ROUTES.ListCategory.as_view()),
    
    path('api/courses/<int:courses_id>', view=API_ROUTES.SingleCourse.as_view()),
    path('api/courses/', view=API_ROUTES.ListCourses.as_view()),
    path('api/courses/search', view=API_ROUTES.SearchCourses.as_view()),
    
    path('api/lesson/<int:lesson_id>', view=API_ROUTES.ListLessons.as_view()),
    
    path('api/profile/<int:profile_id>', view=API_ROUTES.SingleProfile.as_view()),
    path('api/profile/', view=API_ROUTES.ListProfile.as_view()),
    
    path('api/progress/<int:progress_id>', view=API_ROUTES.SingleProgress.as_view()),
    path('api/progress/<int:progress_id>', view=API_ROUTES.ListProgress.as_view()),
    
    path('api/courses/registered', view=API_ROUTES.ListRegisterCourse.as_view()),
]
