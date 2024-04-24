from django.urls import path
from .import views

urlpatterns = [
    path('forticli',views.forticli, name='forticli'),
    path('forticli_modify',views.forticli_modify, name='forticli_modify'),
    path('logs_count', views.logs_count, name='logs_count'),
    path('juniper_policy_create',views.juniper_policy_create, name='juniper_policy_create'),
    
]