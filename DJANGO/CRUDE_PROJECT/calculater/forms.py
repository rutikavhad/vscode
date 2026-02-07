from django import forms
from .models import contact

class contactform(forms.ModelForm):
    class Meta:
        model=contact
        fields='__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'name_input',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'email_input',
                'placeholder': 'Email'
            }),
            'message': forms.Textarea(attrs={
                'class': 'my_text',
                'placeholder': 'Message',
                'rows': 4
            }),
        }


# from django import forms
# from .models import contact

# class contactform(forms.ModelForm):
#     # manual field control (validation rules)
#     name = forms.CharField(max_length=100, required=False)
#     email = forms.EmailField(required=False)
#     message = forms.CharField(required=False)

#     class Meta:
#         model = contact
#         fields = ['name', 'email', 'message']
#         #widegets not work when manual set data 
