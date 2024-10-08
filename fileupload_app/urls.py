# fileupload_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/<slug:slug>/', views.document_detail, name='document_detail'),
]
