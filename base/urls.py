from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register, name='register'),
    path('vote/', views.vote, name='vote'),
    path('voted/', views.voted, name='voted'),
]