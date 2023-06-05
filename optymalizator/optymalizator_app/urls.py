from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('optimize/', views.optimize, name='optimize'),
    path('ref-levels/<int:drug_id>/', views.ref_levels, name='get_ref_levels'),

    path('magic_very_secret_url_that_noone_can_click/', views.clear, name='clear'),
]
