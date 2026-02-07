from django.urls import path,include
from .views import read,create,update,delete,home

urlpatterns = [
    path('',home,name='home'),
    path('read/',read,name='read'),
    path('create/',create,name='create'),
    path('update/<int:id>/',update,name='update'),
    path('delete/<int:id>/',delete,name='delete'),
]
