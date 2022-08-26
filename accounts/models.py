
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extrafields):
        if not email:
            raise ValueError('Please provide an email address')
        user= self.model(username=username, email= self.normalize_email(email), **extrafields)
        user.set_password(password)
        user.save(using = self._db)
        
        return user
    
    def create_superuser(self, email, password, username=None):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
    
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255,unique=True, null=True)
    email= models.EmailField(max_length=255, unique=True)
    name= models.CharField(max_length=100)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD ='email'
    
    
class Profile(models.Model):
    image=models.ImageField(upload_to='images/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=50,default="I love this Expo!")
    location = models.CharField(max_length=60, blank=True)
    
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
    
    def save_profile(self):
            self.save()