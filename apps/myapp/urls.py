from django.urls import path, include
from . import views

urlpatterns = [
       path('', views.index),
    path('register', views.register),
    path('addsong', views.addsong),
    path('displaysong', views.displaysong),
    path('showsong/<id>', views.showsong),
    path('showartist/<id>', views.showartist),
    path('favorite/<id>', views.favorite),
    path('favoriteartist/<id>', views.favoriteartist),
    path('unfavorite/<id>', views.unfavorite),
    path('delete/<id>', views.delete),
    path('createsong', views.createsong),
    path('login', views.login),
    path('logout', views.logout),
]
