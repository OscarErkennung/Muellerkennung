# urls.py
from django.urls import path
from . import views
urlpatterns = [
   path('', views.steuerung, name='steuerung'),
   path('get_status/', views.get_status, name='status'),
]