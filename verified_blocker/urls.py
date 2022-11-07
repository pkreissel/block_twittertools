from django.urls import path

from . import views

urlpatterns = [
    path('verified', views.unfollow, name='verified'),
]
