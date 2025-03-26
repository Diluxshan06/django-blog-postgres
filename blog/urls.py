from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<str:slug>", views.details, name="details"),
    path("old_url", views.old_url, name="old_url"),
    path("new_some_url", views.new_url, name="new_url_reverse"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
]