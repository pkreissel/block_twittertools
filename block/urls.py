from django.urls import path

from . import views

urlpatterns = [
    path('blocklists', views.blocklists, name='blocklists'),
    path("blockapi", views.blockapi, name="blockapi")
]
