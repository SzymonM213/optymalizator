from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('optimize/', views.optimize, name='optimize'),
    path('ref-levels/', views.ref_levels, name='get_ref_levels'),
    path('get-optimize-results/', views.get_optimize_results, name='get_optimize_results'),

    path('magic_very_secret_url_that_noone_can_click/', views.clear, name='clear'),
]
