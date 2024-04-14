from django.urls import path
from .import views

urlpatterns = [
    path('forticli',views.forticli, name='forticli'),
    path('forticli_modify',views.forticli_modify, name='ERROR: duplicate key value violates unique constraint "tbl_appclient_client_name_index"'),
]