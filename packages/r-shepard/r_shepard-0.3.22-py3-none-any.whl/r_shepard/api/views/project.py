import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django_otp.decorators import otp_required

from r_shepard.api.models import Project


@login_required
@otp_required
def project_list_view(request):
    """Display a list of all projects."""
    projects = Project.objects.all()

    # Get system RAM
    system_ram = round(
        os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024**3), 2
    )

    # Get RAM used by currently running containers
    used_ram = sum(
        container.ram
        for project in projects
        for container in project.containers.all()
        if container.is_running
    )

    # Calculate the ratio of used RAM to system RAM
    context = {
        "projects": projects,
        "system_ram": system_ram - 1,
        "used_ram": used_ram,
        "ratio_used_ram_to_system_ram": used_ram / (system_ram - 1) * 100,
    }

    return render(request, "project_list.html", context)


@login_required
@otp_required
def project_detail_view(request, pk):
    """Display the details of a project."""
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        # Handle POST request here
        pass

    # Logic to stop all podman containers for the project
    def stop_all_project_containers():
        pass

    context = {
        "project": project,
    }

    return render(request, "project_detail.html", context)
