from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('choose/', views.upload_view, name='upload-view'),
    path(f'choose/resize', views.resize_view, name='resize-view')
]
