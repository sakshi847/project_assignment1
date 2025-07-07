# payment/urls.py
from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('pay/<str:registration_id>/',                views.pay,        name='pay'),
    path('pay/<str:registration_id>/success/',        views.success,    name='success'),
    path('pay/<str:registration_id>/cancel/',         views.cancel,     name='cancel'),
    path('pay/<str:registration_id>/finalize/',       views.finalize,   name='finalize'),
    
]
