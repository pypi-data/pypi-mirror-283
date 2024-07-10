import os
from typing import Any

from django import forms
from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse
from django.urls import reverse

from .models import Container, Project
from .podman import PodmanError, start_container

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

    # This is only really needed for creating containers from Admin so the logic
    # should correspond to the CreateContainerView
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
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
