from django.urls import path
from . import views



urlpatterns = [
                path('', views.redirect_to_home, name='redirect_to_home'),
                path('home/', views.home, name='home'),
                path('index1/', views.index1, name='index1'),
                path('create_plot/', views.create_plot, name='create_plot')
              ] 