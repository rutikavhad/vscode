from django.db import models

from users.models import Profile,Location
import uuid
from django.core.validators import validate_integer
from .utils import user_list_path

#own inport
from .consts import CARS_BRANDS,TRANSMISSION_OPTIONS

class Listing(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    seller=models.ForeignKey(Profile,on_delete=models.CASCADE)

    #main part

    
    barnd=models.CharField(max_length=24,choices=CARS_BRANDS,default='select')
    model=models.CharField(max_length=50,blank=True)
    milage=models.CharField("MILAGE",max_length=200,validators=[validate_integer],default='0')
    color=models.CharField(("Color"), max_length=25,blank=True)
    description=models.CharField(("Description"),blank=True)
    engin=models.CharField(("Engin"), max_length=50,blank=True)
    transmisson=models.CharField(max_length=10,choices=TRANSMISSION_OPTIONS,default='select')
    location=models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    image=models.ImageField(upload_to=user_list_path,null=True)

    def __str__(self):
        return f'{self.seller.user.username}\'s Car - {self.barnd} & Model= {self.model}'