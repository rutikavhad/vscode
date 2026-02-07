from django.db import models

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=34,blank=True)
    price=models.CharField(blank=True)
    description=models.TextField()

    def __str__ (self):
        return self.name

class User(models.Model):
    name=models.CharField(max_length=34,blank=True)
    age=models.IntegerField(blank=True)

    def __str__(self):
        return self.name