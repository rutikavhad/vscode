from django.urls import path
from .views import calcu,kalp,contects


urlpatterns = [
    path('calcu/',calcu,name='calcu'),
    path('kelp/',kalp,name='kelp'),
    path('contact/',contects,name='contacts')

]
