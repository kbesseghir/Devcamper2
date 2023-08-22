from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
    path('get_current_user/', GetCurrentUser.as_view(), name='get_current_user'),
    path('update_user_info/<int:pk>', UpdateUserInfo.as_view(), name='update_user_info'),
    path('update_password_info/<int:pk>', UpdateUserPassword.as_view(), name='update_user_password'),

    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailsView.as_view(), name='user-detail'),
    path('users/create/', CreateUserView.as_view(), name='user-create'),
    path('users/<int:pk>/update/', UpdateUserView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='user-delete'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",),

    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path( "reset/done/", auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete" ),
   
]
