from django.shortcuts import render
from .models import *
from rest_framework import generics
from .serializers import *
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from permission import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.throttling import UserRateThrottle



class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Maximum number of items per page

class AllBootcamp(generics.ListAPIView):
    queryset =Bootcamp.objects.all()
    serializer_class = BootcampSerializer  
    pagination_class = CustomPagination  
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name', 'average_rating', 'average_cost']  # Fields for sorting
    search_fields = ['name', 'description','country','street','city','address','zipcode']  # Fields for searching
    
class BootcampDetail(generics.RetrieveAPIView):
    queryset =Bootcamp.objects.all()
    serializer_class = BootcampSerializer  


class CreateBootcamp(generics.CreateAPIView):
    throttle_classes = [UserRateThrottle]

    queryset = Bootcamp.objects.all()
    serializer_class = BootcampSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Check if the user has the "publisher" or "admin" role
        if not request.user.is_superuser and not request.user.role == 'publisher':
            return Response({'message': 'You do not have permission to create a bootcamp.'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the user already has a bootcamp
        if request.user.role == 'publisher' and request.user.bootcamp_set.exists():
            return Response({'message': 'You can only create one bootcamp.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response({'message': 'Bootcamp created successfully.'}, status=status.HTTP_201_CREATED) 


class UpdateBootcamp(generics.UpdateAPIView):
    throttle_classes = [UserRateThrottle]

    queryset=Bootcamp.objects.all()
    serializer_class = BootcampSerializer
    permission_classes = [IsAuthenticated]


    def update (self,request,*args,**kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'message': 'You do not have permission to update this bootcamp.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer= self.get_serializer(instance,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()


        return Response({'message': 'Bootcamp updated successfully.'}, status=status.HTTP_200_OK)


class DeleteBootcamp(generics.DestroyAPIView):
    queryset=Bootcamp.objects.all()
    serializer_class = BootcampSerializer
    permission_classes = [IsAuthenticated]

    def Destroy(self, request, *args, **kwargs):
        instance = self.get_object

        if instance.user != request.user:
            return Response({'message': 'You do not have permission to update this bootcamp.'}, status=status.HTTP_403_FORBIDDEN)
        

        self.perform_destroy(instance)

        return Response({'message': 'Bootcamp deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class UploadBootcampPhoto(generics.CreateAPIView):
    throttle_classes = [UserRateThrottle]

    queryset = Bootcamp.objects.all()
    serializer_class = BootcampSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def perform_create(self, serializer):
        serializer.save(photo=self.request.data.get('photo'))