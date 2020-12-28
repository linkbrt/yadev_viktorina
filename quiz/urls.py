from django.urls import path

from . import views


urlpatterns = [
    path('',
         views.index,
         name='index'),
    path('<slug:slug>/success/',
         views.success_page,
         name='success_page'),
    path('<slug:slug>/',
         views.play,
         name='play'),
]
