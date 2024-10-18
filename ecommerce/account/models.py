from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class CustomManager(BaseUserManager):
    def create_user(self,email,user_name, password, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,user_name,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verify', True)
        extra_fields.setdefault('user_type', self.model.USER_TYPE[1][0])

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        if not extra_fields.get('is_active'):
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('user_type') != self.model.USER_TYPE[1][0]:
            raise ValueError('Superuser must have user_type="developer".')

        return self.create_user(email, user_name, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    USER_TYPE = (
        ('visitor','visitor'),
        ('developer','developer')
    )
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=100,unique=True)
    REQUIRED_FIELDS = ['user_name']
    USERNAME_FIELD = 'email'
    user_type = models.CharField(max_length=100, choices=USER_TYPE,default=USER_TYPE[0])
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)

    objects = CustomManager()

    def __str__(self):
        return str(self.email)





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True,null=True)
    email = models.EmailField(max_length=200,blank=True,null=True)
    address = models.CharField(max_length=300,blank=True, null=True)

    country = models.CharField(max_length=100,blank=True, null=True)
    city = models.CharField(max_length=100,blank=True,null=True)
    zipcode = models.CharField(max_length=15, blank=True,null=True)
    phone = models.CharField(max_length=16, blank=True,null=True)
    
    def __str__(self):
        return f"{self.user.user_name}'s profile"



@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)