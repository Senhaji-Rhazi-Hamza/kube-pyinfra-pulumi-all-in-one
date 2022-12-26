from io import StringIO
from pyinfra import host
from pyinfra.facts.server import Command, LsbRelease
from pyinfra.operations import apt, systemd, files


files.put(
    name="Upload a StringIO object",
    src=StringIO('''
    {
        "exec-opts": ["native.cgroupdriver=systemd"]
    }
    '''),
    dest="/etc/docker/daemon.json",
    _sudo=True,
)


apt.packages(
        name="Install apt requirements to use HTTPS",
        packages=["apt-transport-https", "ca-certificates"],
        update=True,
        cache_time=3600,
        _sudo=True,
    )

lsb_release = host.get_fact(LsbRelease)
lsb_id = lsb_release["id"].lower()

apt.key(
    name="Download the Docker apt key",
    src="https://download.docker.com/linux/{0}/gpg".format(lsb_id),
    _sudo=True,
)

dpkg_arch = host.get_fact(Command, command="dpkg --print-architecture", _sudo=True)

add_apt_repo = apt.repo(
    name="Add the Docker apt repo",
    src=(
        f"deb [arch={dpkg_arch}] https://download.docker.com/linux/{lsb_id}"
        f" {lsb_release['codename']} stable"
    ),
    filename="docker-ce-stable",
    _sudo=True,
)

apt.packages(
    name="Install Docker via apt",
    packages=["docker-ce", "containerd.io", "docker-ce-cli"],
    update=add_apt_repo.changed,  # update if we added the repo,
    _sudo=True,
)


# systemd.service(
#     name="Ensure docker is running",
#     service="docker",
#     _sudo=True,
#     running=True,
#     enabled=True,
# )