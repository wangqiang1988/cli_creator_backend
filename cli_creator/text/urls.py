from django.urls import path
from .import views

urlpatterns = [
    path('duplicates',views.duplicates, name='duplicates'),
    path('traversal',views.traversal, name='traversal'),   
]