from django.urls import path
from django.conf import settings
from .views import home_view, main_page,list_view,listing_view,edit_view,profile_update

urlpatterns = [
    path('',main_page,name='main'), # '' do empty for first app 
    path('home/',home_view,name='home'),
    path('list/',list_view,name='list'),
    path('listing/<str:id>',listing_view,name='listing'),
    path('listing/<str:id>/edit/', edit_view, name='edit'),
    path('profile/update/',profile_update, name='profile_update'),

]
