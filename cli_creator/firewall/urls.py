from django.urls import path
from .import views

urlpatterns = [
    path('forticli',views.forticli, name='forticli'),
    path('forticli_modify',views.forticli_modify, name='forticli_modify')
]