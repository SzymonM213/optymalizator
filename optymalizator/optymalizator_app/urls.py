from django.urls import path

from .views import home, search, optimize

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('optimize/', optimize, name='optimize'),
]
