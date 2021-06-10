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
