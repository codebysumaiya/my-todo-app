from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_todo, name="add_todo"),
    path("toggle/<int:pk>/", views.toggle_todo, name="toggle_todo"),
    path("update/<int:pk>/", views.update_todo, name="update_todo"),
    path("delete/<int:pk>/", views.delete_todo, name="delete_todo"),
]
