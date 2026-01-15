
from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    image=forms.ImageField()
    class Meta:
        model = Listing
        fields = {'barnd','model','milage','color','description','engin','transmisson','image'}
