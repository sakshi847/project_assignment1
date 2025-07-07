from django.urls import path
from . import views

app_name = 'studentform'

urlpatterns = [
    path('form/', views.parent_form_view, name='parent_form'),
    path('form/student/', views.student_form_view, name='student_form'),
    path('form/review/', views.review_fee_view, name='review_fee'),
    path('form/payment/', views.initiate_payment, name='initiate_payment'),
]
