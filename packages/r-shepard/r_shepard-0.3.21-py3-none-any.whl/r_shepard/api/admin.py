import os
from typing import Any

from django import forms
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse
from django.urls import reverse

from r_shepard.api.models import Container, Project
from r_shepard.api.podman import (
    PodmanError,
    remove_container,
    start_container,
)

admin.site.site_header = "R-Shepard"
admin.site.site_title = "R-Shepard"
admin.site.index_title = "Admin Area"


class EditContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = "__all__"
        # These fields cannot be edited and are excluded from the edit form
        exclude = [
            "project",
            "container_id",
            "password",
            "port",
            "local_url",
            "is_running",
        ]


class AddContainerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Container
        fields = "__all__"
        exclude = [
            "container_id",
            "is_running",
            "port",
            "local_url",
        ]


class ContainerAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request: Any, obj: Any):
        if obj:  # Edit
            return ["project", "container_id"]
        else:  # Add
            return ["container_id", "image", "tag"]

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            return EditContainerForm
        else:
            return AddContainerForm

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        """Called to save or update an object. Overridden to start the container
        via Podman."""

        # Get system RAM
        system_ram = (
            os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024.0**3)
        )

        # Get  RAM used by currently running containers
        used_ram = sum(
            container.ram
            for container in obj.project.containers.all()
            if container.is_running
        )

        # Check if there are enough RAM available for the container
        if obj.ram > system_ram - used_ram - 1:
            messages.error(request, "Not enough RAM available.")
            return

        # Start container
        try:
            start_container(obj.project, obj, obj.password)
            obj.is_running = True
        except PodmanError as e:
            messages.error(request, str(e))
            return
        super().save_model(request, obj, form, change)

    def delete_model(self, request: HttpRequest, obj: Container) -> None:
        """
        Called to delete an object. Overridden to ensure the container is
        removed via Podman before being deleted from the database.
        """
        try:
            # Attempt to remove the container using Podman
            remove_container(obj.project, obj)
        except PodmanError as e:
            # If there's an error, display a message but proceed with deletion
            messages.error(request, f"Failed to remove container via Podman: {e}")

        # Proceed with the original deletion process
        super().delete_model(request, obj)

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        """
        Called to bulk delete objects. Overridden to ensure each container is
        removed via Podman before being deleted from the database.
        """
        for obj in queryset:
            try:
                # Attempt to remove each container using Podman
                remove_container(obj.project, obj)
            except PodmanError as e:
                # If there's an error, display a message but proceed with deletion
                messages.error(
                    request, f"Failed to remove container {obj.name} via Podman: {e}"
                )

        # Proceed with the original bulk deletion process
        super().delete_queryset(request, queryset)

    # Redirect to project detail page after adding a container
    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse("project_detail", args=[obj.project.pk]))

    def response_change(self, request: HttpRequest, obj: Any) -> HttpResponse:
        return HttpResponseRedirect(reverse("project_detail", args=[obj.project.pk]))


class ProjectAddForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "auto_commit_enabled",
            "git_repo_url",
            "commit_interval",
        ]


class ProjectChangeForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            return ProjectChangeForm
        else:
            return ProjectAddForm

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse("project_list"))

    def response_change(self, request: HttpRequest, obj: Any) -> HttpResponse:
        return HttpResponseRedirect(reverse("project_detail", args=[obj.pk]))


admin.site.register(Container, ContainerAdmin)
admin.site.register(Project, ProjectAdmin)
