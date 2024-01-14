from django.urls import path

from . import views

urlpatterns = [
    path('auth', views.auth, name='auth'),
    path('<str:country>/<str:file>.txt', views.content, name="eula"),
    path('<str:country>/confirm/<str:file>.txt', views.content, name="garbage"),
    path('flipnote/<str:file>.ppm', views.ppmloader, name="ppmloader"),
    path('flipnote/<str:file>.info', views.info, name="info"),
    path('flipnote/<str:file>.dl', views.dl, name="info"),
    path('flipnote/<str:file>.htm', views.flipnote_info, name="info"),
    path('eula_list.tsv', views.eula_list, name="propaganda"),
    path('index.ugo', views.index, name="index"),
    path('newest.ugo', views.newest_list, name="newest"),
    path('channels.ugo', views.categories, name="categories"),
    path('channels/search.ugo', views.others, name="others"),
    path('channels/<str:internal_id>.ugo', views.channels, name="channels"),
    path('channel/<str:internal_id>.ugo', views.channel, name="channel"),
    path('channel/<str:internal_id>.post', views.post_flip, name="post_flip"),
    path('signin.htm', views.signin, name="signin"),
    path('signin/step1.kbd', views.signin_step1, name="step1"),
    path('signin/step2.kbd', views.signin_step2, name="step2"),
    path('error_get.htm', views.error_get, name="error_get"),
]