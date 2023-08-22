from django.urls import path
from .views import *

urlpatterns = [
   path('',AllCourses.as_view(),name='courses'),
   path('<int:pk>/', CourseDetail.as_view(), name='courses-detail'),
   path('CreateCourse/',CreateCourse.as_view(), name='create-coursqe'),
   path('update/<int:pk>/', UpdateCourse.as_view(), name='course-update'),
   path('delete/<int:pk>/', DeleteCourse.as_view(), name='course-delete'),
   path('Bootcamps/<int:bootcamp_id>/courses/', ListBootcampCourses.as_view(), name='bootcamp-courses'),

]