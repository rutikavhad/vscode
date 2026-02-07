from django import forms
from django.contrib.auth.models import User

from .models import Profile


class user_reg(forms.ModelForm):
    email=forms.EmailField(required=False)
    password=forms.CharField(widget=forms.PasswordInput)
    confrom_pass=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username','email']

    def clean(self):
        clean_data=super().clean()
        if clean_data.get('password') !=clean_data.get('confrom_pass'):
            raise forms.ValidationError('password not match')
        return clean_data
        