import subprocess
from datetime import timedelta
from pathlib import Path

from celery import shared_task
from django.utils import timezone

from r_shepard.api.models import Container, Project
from r_shepard.api.podman import PodmanError, is_container_running


@shared_task
def auto_commit():
    # Only do this for projects where auto_commit is enabled
    projects = Project.objects.filter(auto_commit_enabled=True)

    for project in projects:
        print(f"Checking '{project.name}'")
        # Check if it's time to commit
        try:
            now = timezone.now()
            if now - project.last_commit_time >= timedelta(
                minutes=project.commit_interval
            ):
                # Add git origin if .git does not exist
                if not project.git_repo_url:
                    print(f"No Git repository URL for project {project.slug}")
                    continue
                if not Path(f"{project.workspace_path}/.git").exists():
                    result = subprocess.run(
                        ["git", "init"],
                        cwd=project.workspace_path,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                    )
                    print(result.stdout.decode())
                    result = subprocess.run(
                        ["git", "remote", "add", "origin", project.git_repo_url],
                        cwd=project.workspace_path,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                    )
                    print(result.stdout.decode())
                # Commit and push changes
                result = subprocess.run(
                    ["git", "add", "."],
                    cwd=project.workspace_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                print(result.stdout.decode())
                result = subprocess.run(
                    ["git", "commit", "-m", "Auto-commit"],
                    cwd=project.workspace_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                print(result.stdout.decode())
                result = subprocess.run(
                    ["git", "push", project.git_repo_url],
                    cwd=project.workspace_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                print(result.stdout.decode())
                # Update the last commit time
                project.last_commit_time = now
                project.save()
            else:
                print(f"Not time to commit for project {project.slug}")
        except subprocess.CalledProcessError as e:
            print(f"Encountered git error for project {project.slug}: {e}")
        except Exception as e:
            print(f"Failed to auto-commit for project {project.slug}: {e}")


@shared_task
def check_container_status():
    print("Checking container status...")
    for container in Container.objects.all():
        try:
            project = Project.objects.get(id=container.project_id)
            container.is_running = is_container_running(project, container)
            container.save()
        except PodmanError as e:
            print(f"Failed to check container status: {e}")
        else:
            print(f"Container status updated for {container.container_id}")
