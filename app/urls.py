"""exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views, ajax

urlpatterns = [
    path("", views.signin, name="signin"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("announcements/", views.announcements, name="announcements"),
    path("admins/", views.admins, name="admins"),
    #
    #
    # Ajax
    path("announcements/<int:id>/", ajax.get_announcement, name="get_announcement"),
    path("announcements/new/", ajax.add_announcement, name="add_announcement"),
    path(
        "announcements/delete/<int:id>",
        ajax.delete_announcement,
        name="delete_announcement",
    ),
    path("announcements/edit/", ajax.edit_announcement, name="edit_announcement"),
    path(
        "announcements/refresh/",
        ajax.refresh_announcements,
        name="refresh_announcements",
    ),
    path("admins/new/", ajax.add_admin, name="add_admin"),
    path("admins/<int:id>", ajax.add_admin, name="add_admin"),
]
