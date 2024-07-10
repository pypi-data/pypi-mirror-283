import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django_otp.decorators import otp_required

from r_shepard.api.models import Container, Project
from r_shepard.api.podman import (
    PodmanError,
    is_container_running,
    remove_container,
    start_container,
    stop_container,
    update_container_ram,
)


@login_required
@otp_required
def create_container_view(request, project_pk):
    """Create a new container."""
    if request.method == "POST":
        # Initialize message HTML
        message_html = render_to_string("messages.html")

        # Get project from URL
        project = get_object_or_404(Project, pk=project_pk)

        # Get parameters from POST request
        password = request.POST.get("password")
        ram = int(request.POST.get("ram"))
        tag = str(request.POST.get("tag"))
        tag = tag or "4.4.1"

        # Get system RAM
        system_ram = (
            os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024.0**3)
        )

        # Get RAM used by currently running containers
        used_ram = sum(
            container.ram
            for container in project.containers.all()
            if container.is_running
        )

        # Check if there are enough resources available for the container
        if ram > system_ram - used_ram - 1:
            messages.error(request, "Not enough RAM available.")
            message_html = render_to_string(
                "messages.html", {"messages": messages.get_messages(request)}
            )
        else:
            container = Container.objects.create(
                project=project, tag=tag, password=password, ram=ram
            )
            try:
                start_container(project, container, password)
                container.is_running = True
                container.save()
            except PodmanError as e:
                container.delete()
                messages.error(request, str(e))
                message_html = render_to_string(
                    "messages.html", {"messages": messages.get_messages(request)}
                )

        container_list_html = render_to_string(
            "container_list.html", {"project": project}
        )

        return HttpResponse(container_list_html + message_html)


@login_required
@otp_required
def start_container_view(request, project_pk, container_pk):
    """Start a container."""
    if request.method == "POST":
        # Initialize message HTML
        message_html = render_to_string("messages.html")

        # Get project and container from URL
        project = get_object_or_404(Project, pk=project_pk)
        container = get_object_or_404(Container, pk=container_pk)

        # Start container if it is not running
        try:
            if not is_container_running(project, container):
                start_container(project, container)
        except PodmanError as e:
            messages.error(request, str(e))
            message_html = render_to_string(
                "messages.html", {"messages": messages.get_messages(request)}
            )

        # Update container status in the database
        container.is_running = True
        container.save()

        # Render the container list template with the updated project
        container_list_html = render_to_string(
            "container_list.html", {"project": project}
        )

        return HttpResponse(container_list_html + message_html)


@login_required
@otp_required
def stop_container_view(request, project_pk, container_pk):
    """Stop a container."""
    if request.method == "POST":
        # Initialize message HTML
        message_html = render_to_string("messages.html")

        # Get project and container from URL
        project = get_object_or_404(Project, pk=project_pk)
        container = get_object_or_404(Container, pk=container_pk)

        # Stop container if it is running
        try:
            if is_container_running(project, container):
                stop_container(project, container)
        except PodmanError as e:
            messages.error(request, str(e))
            message_html = render_to_string(
                "messages.html", {"messages": messages.get_messages(request)}
            )

        # Update container status in the database
        container.is_running = False
        container.save()

        # Render the container list template with the updated project
        container_list_html = render_to_string(
            "container_list.html", {"project": project}
        )

        return HttpResponse(container_list_html + message_html)


@login_required
@otp_required
def delete_container_view(request, project_pk, container_pk):
    """Delete a container."""
    if request.method == "POST":
        # Initialize message HTML
        message_html = render_to_string("messages.html")

        # Get project and container from URL
        project = get_object_or_404(Project, pk=project_pk)
        container = get_object_or_404(Container, pk=container_pk)

        # Remove container if it is running
        try:
            if is_container_running(project, container):
                remove_container(project, container)
        except PodmanError as e:
            messages.error(request, str(e))
            message_html = render_to_string(
                "messages.html", {"messages": messages.get_messages(request)}
            )

        # Delete container in the database
        container.delete()

        # Render the container list template with the updated project
        container_list_html = render_to_string(
            "container_list.html", {"project": project}
        )

        return HttpResponse(container_list_html + message_html)


@login_required
@otp_required
def change_ram_limit(request, project_pk, container_pk):
    """Temporarily change a container's RAM limit not exceeding what is
    available on the host."""
    # Initialize message HTML
    message_html = render_to_string("messages.html")

    # Get project and container from URL
    project = get_object_or_404(Project, pk=project_pk)
    container = get_object_or_404(Container, pk=container_pk)

    # Get system resources
    system_ram = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024.0**3)

    # Get RAM used by currently running containers
    used_ram = sum(
        container.ram for container in project.containers.all() if container.is_running
    )

    # Get new RAM limit from POST request
    new_ram = int(request.POST.get("new_ram"))

    # Check if there is enough RAM available for the new limit
    if new_ram > system_ram - used_ram - 1:
        messages.error(request, "Not enough RAM available.")
        message_html = render_to_string(
            "messages.html", {"messages": messages.get_messages(request)}
        )
    else:
        container.ram = new_ram
        update_container_ram(project, container)
        container.save()

    # Render the container list template with the updated project
    container_list_html = render_to_string("container_list.html", {"project": project})

    return HttpResponse(container_list_html + message_html)
