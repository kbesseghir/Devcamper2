from django.db import models
from Authentication.models import CustomUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.core.validators import MinValueValidator



class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    weeks = models.CharField(max_length=20)
    tuition = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    minimum_skill = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'), 
        ('advanced', 'Advanced')
          ])
    scholarship_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    bootcamp = models.ForeignKey('Bootcamps.Bootcamp', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Courses'

@receiver (post_save,sender=Course,)
def update_average_cost_on_save(sender,instance,**kagr):

    bootcamp = instance.bootcamp

    average_cost=Course.objects.filter(bootcamp=bootcamp).aggregate(models.Avg('tuition'))['tuition__avg']
    if average_cost is not None:
        bootcamp.average_cost = round(average_cost,2)
        bootcamp.save()

@receiver(post_delete, sender=Course)
def update_average_cost_on_delete(sender, instance, **kwargs):
    bootcamp = instance.bootcamp
    average_cost = Course.objects.filter(bootcamp=bootcamp).aggregate(models.Avg('tuition'))['tuition__avg']
    if average_cost is not None:
        bootcamp.average_cost = round(average_cost, 2)
    else:
        bootcamp.average_cost = None
    bootcamp.save()


@receiver(post_save, sender=Course)
def update_average_cost_on_tuition_update(sender, instance, **kwargs):
    if not instance._state.adding and instance.tuition != instance.tuition:
        update_average_cost_on_save(sender, instance, **kwargs)