from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_name>", views.view_page, name="view_page"),
    path("newpage", views.new_page, name="new_page"),
    path("wiki/editpage/<str:page_name>", views.edit_page, name="edit_page"),
    path("search/", views.searched_pages, name="search_page")
]
