import subprocess

from django.conf import settings
from podman import PodmanClient
from podman.errors import NotFound

from .models import Container, Project

# Get the podman settings from the Django settings
PODMAN_HOST_ADDRESS = settings.PODMAN_HOST_ADDRESS
PODMAN_SOCKET = settings.PODMAN_SOCKET

# These are versions of the rocker/rstudio image that recognize that they
# are in a rootless podman container and adjust the paths accordingly. The
# feature was applied in this commit:
# https://github.com/rocker-org/rocker-versioned2/commit/8ab4e7d01acaf3070f4628251897b779b09ca1a2
SUPPORTED_RSTUDIO_VERSIONS_WITH_ROOT_PATCH = [
    # 4.1
    "4.4.1",
    "4.4.0",
    # 4.3
    "4.3.2",
    "4.3.1",
    "4.3.0",
    # 4.2
    "4.2.3",
    "4.2.2",
    "4.2.1",
    "4.2.0",
    # 4.1
    "4.1.3",
    # 4.0
    "4.0.5",
]

# These are the version where the user is still 'rstudio' and not 'root'
SUPPORTED_RSTUDIO_VERSIONS_WITHOUT_ROOT_PATCH = [
    # 4.1
    "4.1.2",
    "4.1.1",
    "4.1.0",
    # 4.0
    "4.0.4",
    "4.0.3",
    "4.0.2",
    "4.0.1",
    "4.0.0",
]

# 'container' always refers to the Container model instance whereas
# 'podman_container' refers to the podman container instance


class PodmanError(Exception):
    """Base class for Podman exceptions."""

    pass


def get_podman_container(client, project, container):
    """Get the podman container object if it exists, else return None."""
    try:
        return client.containers.get(f"rstudio_{project.slug}_{container.container_id}")
    except NotFound:
        return None


def start_and_save_container(podman_container, container):
    """Start the podman container and save the container details."""
    podman_container.start()
    podman_container.reload()

    container.port = podman_container.ports["8787/tcp"][0]["HostPort"]
    container.local_url = f"http://{PODMAN_HOST_ADDRESS}:{container.port}"
    container.save()

    print(f"Container started at {container.local_url}")


def create_rstudio_container_config(project, container, password):
    """Create the container configuration. Right now, it only supports RStudio."""

    # Specify the image, name, and other configurations for the container
    config = {
        "image": f"{container.image_host}/{container.image}:{container.tag}",
        "name": f"rstudio_{project.slug}_{container.container_id}",
        "detach": True,
        "ports": {"8787/tcp": container.port},  # Assuming default RStudio port
        "environment": {
            "PASSWORD": password,  # Set the PASSWORD environment variable for RStudio
            "ROOT": "TRUE",
        },
        "mem_limit": f"{container.ram}g",
        # Restart the container if it stops
        "restart_policy": {"Name": "always"},
        "mounts": [
            {
                "type": "bind",
                "source": f"{project.data_path}",
                "target": "/data",
                "read_only": False,
            },
        ],
    }

    # If user requests a version with the root patch, mount the workspace to
    # the /root directory
    if container.tag in SUPPORTED_RSTUDIO_VERSIONS_WITH_ROOT_PATCH:
        config["mounts"].append(
            {
                "type": "bind",
                "source": f"{project.workspace_path}",
                "target": f"/root/{project.slug}",
                "read_only": False,
            },
        )
        # Set the username to root, so it can be displayed in the UI
        container.username = "root"
        container.save()
        return config

    # If user requests a version without the root patch, mount the workspace
    # to the /home/rstudio directory
    elif container.tag in SUPPORTED_RSTUDIO_VERSIONS_WITHOUT_ROOT_PATCH:
        (
            config["mounts"].append(
                {
                    "type": "bind",
                    "source": f"{project.workspace_path}",
                    "target": f"/home/rstudio/{project.slug}",
                    "read_only": False,
                },
            ),
        )
        # Set the username to rstudio, so it can be displayed in the UI
        container.username = "rstudio"
        container.save()
        return config

    # Force user to specify a supported version
    else:
        raise PodmanError(
            "Unsupported RStudio version. Only versions 4.x.x are currently supported."
        )


def start_container(project: Project, container: Container, password: str = None):
    """Start the container."""
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        podman_container = get_podman_container(client, project, container)

        if podman_container is not None:
            print("Container already exists. No need to create.")
            if podman_container.status != "running":
                print("Starting container...")
                start_and_save_container(podman_container, container)
        else:
            print("Container does not exist creating...")
            container_config = create_rstudio_container_config(
                project, container, password
            )
            try:
                client.images.pull(container_config["image"])
                podman_container = client.containers.create(**container_config)
                start_and_save_container(podman_container, container)
            except Exception as e:
                # TODO Handle cases where the container creation fails because
                # of a missing directory and create it during project creation
                # ideally
                raise PodmanError(f"Failed to start container: {e}")


def stop_container(project: Project, container: Container):
    """Stop the container."""
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        try:
            podman_container = client.containers.get(
                f"rstudio_{project.slug}_{container.container_id}"
            )
            podman_container.stop()
        except Exception as e:
            raise PodmanError(f"Failed to stop container: {e}")


def remove_container(project: Project, container: Container):
    """Remove the container."""
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        try:
            podman_container = client.containers.get(
                f"rstudio_{project.slug}_{container.container_id}"
            )
            podman_container.remove(force=True)
            print("Container removed.")
        except Exception as e:
            raise PodmanError(f"Failed to remove container: {e}")


def prune_containers():
    """Prune all stopped containers."""
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        try:
            client.containers.prune()
            print("Containers pruned.")
        except Exception as e:
            raise PodmanError(f"Failed to prune containers: {e}")


def is_container_running(project: Project, container: Container):
    """Check if the container is running."""
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        try:
            podman_container = client.containers.get(
                f"rstudio_{project.slug}_{container.container_id}"
            )
            return podman_container.status == "running"
        except Exception as e:
            raise PodmanError(f"Failed to get container status: {e}")


def update_container_ram(project: Project, container: Container):
    """Update the RAM allocation for the container."""
    try:
        cmd = [
            "podman",
            "container",
            "update",
            f"rstudio_{project.slug}_{container.container_id}",
            "--memory",
            f"{container.ram}g",
        ]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise PodmanError(f"Failed to update container RAM allocation: {e}")
