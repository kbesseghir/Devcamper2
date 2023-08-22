from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import Authentication
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm

from Authentication.models import *
from .serializers import *
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle
from permission import *
from .models import *

import logging

class UserRegistration(generics.CreateAPIView):
    
    serializer_class = UserSerializer 
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            user = serializer.data
            if 'password' in user:
                user.pop('password')

            logger = logging.getLogger(__name__)
            logger.info(f"User registered: {user['email']}")

            headers = self.get_success_headers(serializer.data)
            return Response(user, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"User registration failed: {e}")
            raise

class UserLogin(APIView):
    throttle_classes = [UserRateThrottle]  # Add rate limiting to this view
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        logger = logging.getLogger(__name__)

        if email is None or password is None:
            logger.warning('Login attempt with missing email or password')
            return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            EmailValidator(email)
        except ValidationError:
            logger.warning('Login attempt with invalid email format')
            return Response({'error': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            logger.warning('Login attempt with non-existent user')
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            logger.warning('Login attempt with invalid password')
            return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            logger.warning('Login attempt with disabled user account')
            return Response({'error': 'User account is disabled.'}, status=status.HTTP_403_FORBIDDEN)

        logger.info(f"User logged in: {user.email}")
        refresh = RefreshToken.for_user(user)
        response = Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
        response.set_cookie('token', refresh.access_token, max_age=30 * 24 * 60 * 60, secure=True, httponly=True)
        return response

class UserLogout(APIView):
    def post(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)

        response = Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        response.delete_cookie('token')
        logger.info('User logged out')
        return response



class GetCurrentUser(generics.RetrieveAPIView):
    permission_classes =(IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UpdateUserInfo(generics.RetrieveUpdateAPIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

class UpdateUserPassword(generics.RetrieveUpdateAPIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdatePasswordSerializer
    queryset = CustomUser.objects.all()

    
    def update(self, request, *args, **kwargs):
        user = self.get_object()  # Fetch the authenticated user
        serializer = self.get_serializer(user, data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            if not user.check_password(old_password):
                return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
            
            new_password = serializer.validated_data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class CreateUserView(generics.CreateAPIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


class UserListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetailsView(generics.RetrieveAPIView):
    permission_classes = (IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UpdateUserView(generics.UpdateAPIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = (IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class DeleteUserView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = CustomUser.objects.all()





