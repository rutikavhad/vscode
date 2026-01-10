from django.urls import path
from django.conf import settings
from .views import home_view, main_page

urlpatterns = [
    path('',main_page,name='main'), # '' do empty for first app 
    path('home/',home_view,name='home')
]
