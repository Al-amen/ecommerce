from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True,null=True)
    address = models.CharField(max_length=300,blank=True, null=True)
    country = models.CharField(max_length=100,blank=True, null=True)
    city = models.CharField(max_length=100,blank=True,null=True)
    zipcode = models.CharField(max_length=15, blank=True,null=True)
    phone = models.CharField(max_length=16, blank=True,null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"



@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)