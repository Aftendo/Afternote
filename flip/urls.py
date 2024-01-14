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
    path('hot.ugo', views.ugo_list, name="ugolist"),
    path('post/flipnote.post', views.post_flip, name="post_real")
]