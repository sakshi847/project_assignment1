from django.urls import path
from dashboard import views as dashboard_views
from . import views

urlpatterns = [
    path('home/', views.home, name='dashboard_home'),
    path('logout/', dashboard_views.logout_view, name='logout'),
]

