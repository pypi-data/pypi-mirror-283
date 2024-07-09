# src/urls.py
from django.urls import path
from .views import upload_file, success_view

app_name = 'xlsxExporter'

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('success/', success_view, name='success'),
]
