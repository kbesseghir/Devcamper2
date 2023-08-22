
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('Auth/',include('Authentication.urls')),
    path('Bootcamps/',include('Bootcamps.urls')),
    path('Courses/',include('Courses.urls')),
    path('Reviews/',include('Reviews.urls'))



]
