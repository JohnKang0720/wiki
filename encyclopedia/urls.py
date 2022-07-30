from django.urls import path
from . import util
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("randompage", views.randomPage, name="randompage"),
    path("searchpage", views.searchPage, name="searchpage"),
    path("pages/<str:title>", views.pages, name="pages"),
    path("edit/<str:title>", views.edit, name="edit")                                                                                    
]
