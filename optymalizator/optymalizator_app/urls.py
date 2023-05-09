from django.urls import path

from .views import home, search, optimize, get_search_results, get_optimize_results

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('search/optimize/', optimize, name='optimize'),
    path('get_search_results/', get_search_results, name='get_search_results'),
    path('get_optimize_results/', get_optimize_results, name='get_optimize_results')
]
