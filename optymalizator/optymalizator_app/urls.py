from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('get_search_results/', views.get_search_results, name='get_search_results'),
    path('optimize/', views.optimize, name='optimize'),
]
