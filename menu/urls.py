from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('home/', my_view, name='home'),
    path('about/', my_view, name='about'),
    path('contact/', my_view, name='contact'),
    path('home/about/', my_view, name='home/about'),
    path('home/contact/', my_view, name='home/contact'),
    path('about/contact/', my_view, name='about/contact'),
    path('about/home/', my_view, name='about/home'),
    path('home/contact/contact/', my_view, name='home/contact/contact'),

]