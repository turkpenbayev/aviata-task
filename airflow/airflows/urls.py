from django.urls import path

from .views import results, search

urlpatterns = [
    path('search/', search),
    path('results/<uuid:search_id>/<str:currency>/', results)
]
