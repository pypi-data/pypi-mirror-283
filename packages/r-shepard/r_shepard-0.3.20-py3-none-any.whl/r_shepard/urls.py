"""
URL configuration for r_shepard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from django.views.generic.base import RedirectView
from two_factor.admin import AdminSiteOTPRequired
from two_factor.urls import urlpatterns as tf_urls

from r_shepard.api.views.container import (
    change_ram_limit,
    create_container_view,
    delete_container_view,
    start_container_view,
    stop_container_view,
)
from r_shepard.api.views.project import (
    project_detail_view,
    project_list_view,
)

admin.site.__class__ = AdminSiteOTPRequired

urlpatterns = [
    # Auth
    path("", include(tf_urls)),
    # Redirect empty path to /projects
    path("", RedirectView.as_view(url="/projects", permanent=True)),
    # Admin site
    path("admin/", admin.site.urls),
    # Project views
    path("projects/", project_list_view, name="project_list"),
    path("projects/<int:pk>/", project_detail_view, name="project_detail"),
    # Container views
    path(
        "projects/<int:project_pk>/containers/new/",
        create_container_view,
        name="create_container",
    ),
    path(
        "projects/<int:project_pk>/containers/<int:container_pk>/change_ram_limit/",
        change_ram_limit,
        name="change_ram_limit",
    ),
    path(
        "projects/<int:project_pk>/containers/<int:container_pk>/start/",
        start_container_view,
        name="start_container",
    ),
    path(
        "projects/<int:project_pk>/containers/<int:container_pk>/stop/",
        stop_container_view,
        name="stop_container",
    ),
    path(
        "projects/<int:project_pk>/containers/<int:container_pk>/delete/",
        delete_container_view,
        name="delete_container",
    ),
]
