from django.urls import path

from . import views

urlpatterns = [
    path('verified', views.verified, name='verified'),
    path('unfollow', views.unfollow, name='unfollow'),
]
