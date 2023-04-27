from django.urls import path
from . import views

urlpatterns = [
    path('transcribe/', views.transcribe_video, name='transcribe_video'),
]
