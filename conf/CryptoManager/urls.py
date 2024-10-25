from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('certificates/', get_user_certificates, name='get_user_certificates'),
    path('certificates/<int:id>/', get_certificate,name='get_certificate'),
    path('create_certificates/', issue_certificate, name='post_certificate'),
    path('check_status/<int:token_id>/', check_status, name='check-status'),
    path('get_bytecode/', get_bytecode_and_abi),
]