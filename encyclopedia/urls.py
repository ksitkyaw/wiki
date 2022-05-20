from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>", views.entry, name='entry'),
    path("createpage", views.create, name='create'),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("random", views.randompage, name='random')
]
#the fourth path will be redirected from second path so i added 'wiki/' as I didn't know how to code paths without being relative to current path
#the path containing variable like second and fourth path cannot be code with their name at least I don't know how to in this moment