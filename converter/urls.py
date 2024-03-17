from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_page, name='upload_page'),
    path('upload/', views.convert_file, name='convert_file'),
    path('download/', views.download_view, name='download_view'),
    path('uploadpage/', views.upload_page, name='upload_page'),
]
