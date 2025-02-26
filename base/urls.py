from django.urls import path
from . import views



urlpatterns = [
    path('home/', views.home, name='home'),
    path('vote/', views.voting_view, name='vote'),
    path('', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('register/', views.register, name='register'),
]
