from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('single/', views.singlePlay, name='single'),
    path('duration/', views.durationPlay, name='duration'),
]

