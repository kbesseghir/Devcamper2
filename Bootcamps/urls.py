from django.urls import path
from .views import *

urlpatterns = [
   path('',AllBootcamp.as_view(),name='bootcamps'),
   path('<int:pk>/', BootcampDetail.as_view(), name='bootcamp-detail'),
   path('CreateBootcamp/',CreateBootcamp.as_view(), name='create-bootcamp'),
   path('update/<int:pk>/', UpdateBootcamp.as_view(), name='bootcamp-update'),
   path('delete/<int:pk>/', DeleteBootcamp.as_view(), name='bootcamp-delete'),
   path('<int:pk>/upload-photo/', UploadBootcampPhoto.as_view(), name='upload-bootcamp-photo'),

]
