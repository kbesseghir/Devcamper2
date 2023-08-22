from django.db import models
from Authentication.models import CustomUser
from django.contrib.gis.db import models
from django.contrib.gis.db.models import PointField
from django.core.validators import MinValueValidator,MaxValueValidator
from Courses.models import Course
from Reviews.models import Review

from django.db import models
from django.utils.text import slugify
from geopy.geocoders import Nominatim  # You can use a geocoding library like geopy

class Bootcamp(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length=500)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255)
    
    # Location
    # coordinates = models.PointField(geography=True, blank=True, null=True)
    formatted_address = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
  
    average_rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    average_cost = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to='bootcamps/', default='no-photo.jpg')
    housing = models.BooleanField(default=False)
    job_assistance = models.BooleanField(default=False)
    job_guarantee = models.BooleanField(default=False)
    accept_gi = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Bootcamps' 
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

    
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        Course.objects.filter(bootcamp=self).delete()
        Review.objects.filter(bootcamp=self).delete()
        super().delete(*args, **kwargs)








