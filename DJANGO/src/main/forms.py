
from django import forms
from .models import Listing
from .models import Profile,Location

class ListingForm(forms.ModelForm):
    image=forms.ImageField()
    class Meta:
        model = Listing
        fields = {'barnd','model','milage','color','description','engin','transmisson','image'}



class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['user','photo','bio','phone_number','location']


class LocationForm(forms.ModelForm):
    class Meta:
        model=Location
        fields=['address_1','address_2','city','state','zip_code']
