from rest_framework import serializers
from .models import *

class BootcampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bootcamp
        fields = '__all__'