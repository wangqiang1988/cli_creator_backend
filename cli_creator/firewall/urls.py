from django.urls import path
from .import views

urlpatterns = [
    path('forticli',views.forticli, name='forticli'),
    path('forticli_modify',views.forticli_modify, name='forticli_modify'),
    path('logs_count', views.logs_count, name='logs_count'),
    path('juniper_policy_create',views.juniper_policy_create, name='juniper_policy_create'),
    path('juniper_address_create',views.juniper_address_create, name='juniper_address_create'),
    path('food_add',views.food_add, name='food_add'),
    path('print_foodlist',views.print_foodlist, name='print_foodlist'),
]