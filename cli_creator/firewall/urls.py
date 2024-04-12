from django.urls import path
from .import views

urlpatterns = [
    path('forticli',views.forticli, name='forticli'),
]