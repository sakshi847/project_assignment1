from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.otp_login, name='otp_login'),
]
