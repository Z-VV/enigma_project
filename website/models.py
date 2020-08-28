from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    week_subscription = models.BooleanField(default=False)
    d = datetime(1900,1,1,12,0,0,0)
    week_payment_date = models.DateTimeField(default=d)
    month_subscription= models.BooleanField(default=False)
    month_payment_date = models.DateTimeField(default=d)
    app_download = models.BooleanField(default=False)
    app_download_time = models.DateTimeField(default=d)
    trial_finished = models.BooleanField(default=False)
    trial_token = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Message(models.Model):
    name = models.CharField(name='name',max_length=50)
    email = models.CharField(name='email',max_length=50)
    text = models.TextField(name = 'text',unique=True)

    def __str__(self):
        return self.name