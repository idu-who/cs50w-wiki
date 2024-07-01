from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("search-results/<str:query>/", views.search_results, name="search_results"),
    path("wiki/<str:title>/", views.entry, name="entry"),
]
