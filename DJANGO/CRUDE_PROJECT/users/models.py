from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.IntegerField(("phone"),max_length=15,null=True,blank=True)
    age=models.CharField(("Age"), max_length=50,blank=True)
    Gender=[
        ('M','male'),
        ('F','female'),
        ('O','other')

    ]
    gender=models.CharField(max_length=1,choices=Gender)
   

    def __str__(self):
        return self.user.username


