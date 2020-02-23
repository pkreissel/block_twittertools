from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('callback', views.callback, name="callback"),
    path('api', views.api, name="api"),
    path("logout", views.logout, name="logout")
]
