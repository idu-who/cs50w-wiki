from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("search-results/<str:query>/", views.search_results, name="search_results"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("create-page/", views.create_entry, name="create_entry"),
    path("edit-page/<str:title>/", views.edit_entry, name="edit_entry"),
    path("random-page/", views.random_entry, name="random_entry"),
]
