from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):

    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user =models.OneToOneField(User, null=True, blank=True, related_name="customer", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    country_code = models.CharField(max_length=3, blank=True)
    phone_number = models.CharField(max_length=12, blank=True, unique=True)
    gender = models.CharField(max_length=10 , choices = GENDER)
    birthdate = models.DateField(blank=True)
    avatar = models.ImageField(max_length=255, upload_to='images/', blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    otp = models.IntegerField(null=True, blank=True, unique=True) 

    def __str__(self) -> str:
        return f"{self.first_name} - {self.phone_number}"
    
    
    






