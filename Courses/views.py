from django.shortcuts import render
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from permission import *
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework import generics
from .serializers import *
from rest_framework.throttling import UserRateThrottle




class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Maximum number of items per page

class AllCourses(generics.ListAPIView):
    queryset =Course.objects.all()
    serializer_class =   CourseSerializer
    pagination_class = CustomPagination  
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    # ordering_fields = ['name', 'average_rating', 'average_cost']  # Fields for sorting
    search_fields = ['titel', 'description','bootcamp']  # Fields for searching


class CourseDetail(generics.RetrieveAPIView):
    queryset =Course.objects.all()
    serializer_class = CourseSerializer
    

class CreateCourse(generics.CreateAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        title = serializer.validated_data['title']
        if Course.objects.filter(title=title).exists():
          return Response({'message': 'Course with this title already exists.'}), 
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({'message': 'Course created successfully.'}, status=status.HTTP_201_CREATED) 



class UpdateCourse(generics.RetrieveUpdateAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrAdmin]  # Use the custom permission class

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Course updated successfully.'}, status=status.HTTP_200_OK)
    


class DeleteCourse(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [IsOwnerOrAdmin]  # Use the custom permission class

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response({'message': 'Course deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    


class ListBootcampCourses(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        bootcamp_id = self.kwargs['bootcamp_id']
        return Course.objects.filter(bootcamp_id=bootcamp_id)
