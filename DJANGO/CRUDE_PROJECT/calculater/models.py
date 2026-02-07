from django.db import models

# Create your models here.

class contact(models.Model):
    name=models.CharField(max_length=50,blank=True)
    email=models.EmailField(max_length=254,blank=True)
    message=models.CharField(blank=True)