from django.urls import path
from .views import *

urlpatterns = [
   path('',AllReviews.as_view(),name='Reviews'),
   path('<int:pk>/', ReviewDetail.as_view(), name='Reviews-detail'),
   path('CreateReview/',CreateReview.as_view(), name='create-coursqe'),
   path('update/<int:pk>/', UpdateReview.as_view(), name='Review-update'),
   path('delete/<int:pk>/', DeleteReview.as_view(), name='Review-delete'),
   path('Bootcamps/<int:bootcamp_id>/Reviews/', ListBootcampReviews.as_view(), name='bootcamp-Reviews'),

]