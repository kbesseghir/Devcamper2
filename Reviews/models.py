from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from Authentication.models import CustomUser
from django.core.validators import MinValueValidator,MaxValueValidator


class Review(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    bootcamp = models.ForeignKey('Bootcamps.Bootcamp', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 


   

@receiver (post_save,sender=Review,)
def update_average_rating_on_save(sender,instance,**kagr):

    bootcamp = instance.bootcamp

    avg_rating = Review.objects.filter(bootcamp=bootcamp).aggregate(models.Avg('rating'))['rating__avg']
    if avg_rating is not None:
            bootcamp.average_rating = round(avg_rating, 1)
            bootcamp.save()
    else:
           bootcamp.average_rating = None
           bootcamp.save()




@receiver(post_delete, sender=Review)
def update_average_rating_on_delete(sender, instance, **kwargs):
    bootcamp = instance.bootcamp
    average_rating = Review.objects.filter(bootcamp=bootcamp).aggregate(models.Avg('rating'))['rating__avg']
    if average_rating is not None:
        bootcamp.average_rating = round(average_rating, 2)
    else:
        bootcamp.average_rating = None
    bootcamp.save()


@receiver(post_save, sender=Review)
def update_average_rating_on_rate_update(sender, instance, **kwargs):
    if not instance._state.adding and instance.rating != instance.rating:
        update_average_rating_on_save(sender, instance, **kwargs)

