from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('optimize/', views.optimize, name='optimize'),

    path('magic_very_secret_url_that_noone_can_click/', views.clear, name='clear'),
]
