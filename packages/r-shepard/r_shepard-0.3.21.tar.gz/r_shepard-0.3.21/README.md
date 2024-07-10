# r-shepard

![Coverage Status](./coverage-badge.svg)

Simple, self-hosted solution for collaborative (not real-time) R computing leveraging podman,
RStudio, and Tailscale.

Built with Django and HTMX.

## Develop

First start the development environment using [devenv](https://devenv.sh):

```bash
devenv up # starts redis-server, celery worker (doing the task) and celery beat (scheduling the task)
run-tests # runs the tests
```

Then start the Django development server:

```bash
python manage.py runserver # This could also be done from your IDE / debugging environment
```

## Installation instructions (Ubuntu 22.04).

### Requirements

- Install [podman](https://podman.io/docs/installation) (used for running
  RStudio containers), git (needed for auto-commit functionality), and
  redis-server (needed for celery which is used for scheduling recurring tasks).

```bash
sudo apt install podman git redis-server
```

### Prepare the environment

First, it's advised to create a new user with a strong password for running the
application:

```bash
sudo useradd r-shepard
```

This user needs be able to run `podman` without `sudo`. To do this, assign
subordinate group and user ID ranges to the user:

```bash
echo "r-shepard:100000:65536" | sudo tee -a /etc/subuid
echo "r-shepard:100000:65536" | sudo tee -a /etc/subgid
```

But since `r-shepard` wants to speak with a Podman socket, it's a bit more
complicated. To really use podman without superuser privileges, you need to
ensure that there is a podman socket running for the user. First you need to
install the `systemd-container` package and then enable the podman socket for
the correct user.

```bash
sudo apt install systemd-container # This gives us machinectl
sudo loginctl enable-linger r-shepard # This ensures that the user's systemd instance is running after the user logs out or a reboot
sudo machinectl shell r-shepard@ /bin/systemctl --user enable --now podman.socket # This enables the podman.socket for the user
```

Then, switch to your new system user and install the application:

```bash
sudo su -l r-shepard  # Switch to the new user
pip install r-shepard # Install the application via PyPi
```

At this point you should have the `r-shepard` command available. You can check this by running:

```bash
r-shepard --help
```

You can now use this command to manage the application. This command is a
wrapper around the `manage.py` command of the Django application. In order to
function properly, a few environment variables need to be set. The easiest way is to create a file in the user's home directory:

```bash
# /home/r-shepard/.env
DEBUG=False
DB_PATH=/home/r-shepard/db.sqlite
SECRET_KEY=<your secret key>
ALLOWED_HOSTS=klips28.osi.uni-mannheim.de # This should be the hostname of the server
CSRF_TRUSTED_ORIGINS=https://klips28.osi.uni-mannheim.de # This should be the hostname of the server including the protocol
PODMAN_HOST_ADDRESS=klips28.osi.uni-mannheim.de # This should be the hostname of the server
PODMAN_SOCKET=unix:/run/user/1019/podman/podman.sock # This should be the path to the podman socket, which can be found by running `systemctl --machine r-shepard@ --user show podman.socket | grep Listen`
DATA_DIR=/home/r-shepard/data
WORKSPACE_DIR=/home/r-shepard/workspaces
STATIC_ROOT=/var/www/r-shepard/
```

Ensure that all the locations mentioned in thie file exist and are writable by the user.

Now, you can create the database by applying the migrations and collecting the static files:

```bash
r-shepard migrate
r-shepard collectstatic
```

Then, you're in principle ready to run the application:

```bash
daphne -b 0.0.0.0 -p 8000 r_shepard.asgi:application
```

Since you might want to restart this in case of a crash, it's a good idea to use
a process manager like `systemd` to manage the application. In total, you need three files:

One for the application itself:

```ini
# /etc/systemd/system/r-shepard.daphne.service
[Unit]
Description=Daphne ASGI server
After=network.target

[Service]
EnvironmentFile=/home/r-shepard/.env
ExecStart=/home/r-shepard/.local/bin/daphne -b 127.0.0.1 -p 8000 r_shepard.asgi:application
WorkingDirectory=/home/r-shepard
User=r-shepard
Group=r-shepard
Restart=always
SyslogIdentifier=daphne

[Install]
WantedBy=multi-user.target
```

One for the celery worker:

```ini
# /etc/systemd/system/r-shepard.celery.service
[Unit]
Description=Celery Service
After=network.target

[Service]
EnvironmentFile=/home/r-shepard/.env
WorkingDirectory=/home/r-shepard
ExecStart=/home/r-shepard/.local/bin/celery -A r_shepard worker --loglevel=info
User=r-shepard
Group=r-shepard
Restart=always
SyslogIdentifier=celery

[Install]
WantedBy=multi-user.target
```

and one for the celery beat scheduler:

```ini
# /etc/systemd/system/r-shepard.celery-beat.service
[Unit]
Description=Celery Beat Service
After=network.target

[Service]
EnvironmentFile=/home/r-shepard/.env
WorkingDirectory=/home/r-shepard
ExecStart=/home/r-shepard/.local/bin/celery -A r_shepard beat --loglevel=info
User=r-shepard
Group=r-shepard
Restart=always
SyslogIdentifier=celery-beat

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable r-shepard.*
sudo systemctl start r-shepard.*
```

Now, if you want the containers managed by R-Shepard to restart automatically after a reboot, the `podman-restart` service needs to be enabled for the user as well:

```bash
cp /lib/systemd/system/podman-restart.service /lib/systemd/user/
machinectl shell r-shepard@ /bin/systemctl --user enable podman-restart
machinectl shell r-shepard@ /bin/systemctl --user start podman-restart
```

### Open ports

If you want to access application from inside the your network, you may need to open
the ports 40000 to 41000. In case you use `ufw`, you can do this by running:

```bash
sudo ufw allow 40000:41000/tcp # This could be improved by allowing traffic only from the OSI network (or using something like Nebula)
```

## Minimum Viable Product

- [x] Add installation instructions for Ubuntu 22.04
- [x] ~~[gitwatch](https://github.com/gitwatch/gitwatch?tab=readme-ov-file) integration~~ Rolled my own solution. Need to document and integrate it into the UI.
- [x] Remove tailscale as `tailscale serve/funnel` does not work (see [this issue](https://github.com/tailscale/tailscale/issues/10693#issuecomment-2183277632)).
- [x] Publish on PyPi
- [x] ~~Add views for project creation~~ Django admin is enough for now.
- [x] Test R Project/Package management inside the container (e.g. `renv`)
- [x] Add Volume management
- [x] Setup Frontend framework (e.g. ~~Bootstrap~~, PicoCSS)
- [x] Setup 2FA
- [x] Add Tailscale Serve integration
- [x] Add basic container management via podman
- [x] Add basic views for projects and container management
- [x] ~~Add Tailscale Funnel integration~~ Not needed right now
- [x] ~~Make it possible to assign users to projects (only superusers should be able to create projects and assign users to them)~~ Not needed right now

## Potential Future Features

- LDAP integration
- container-specific and user-specific auto-commits
- `code-server` integration
