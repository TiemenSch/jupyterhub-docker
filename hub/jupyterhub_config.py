"""Configuration file for Jupyter Hub"""
from dockerspawner import DockerSpawner
import os
import shutil
import netifaces
import binascii

c = get_config()

# Root directory for JupyterHub
root_dir = os.path.dirname(__file__)

# Skeleton directory containing default files for all users (copied in)
skeleton_dir = os.path.join(root_dir, 'skeleton')

# Demo directory overwritten / reset on each login
demo_dir = os.path.join(root_dir, 'demo')

# Persistent storage directory
volume_dir = '/mnt/work/jupyterhub'

# DockerSpawner notebook directory
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'

# uid, gid of docker user
uid = 1000
gid = 1000


class LocalDockerSpawner(DockerSpawner):
    def start(self):
        user_dir = os.path.join(volume_dir, self.user.name)
        if not os.path.exists(user_dir):
            shutil.copytree(skeleton_dir, user_dir)

        user_demo = os.path.join(user_dir, 'demo')
        if os.path.exists(user_demo):
            shutil.rmtree(user_demo)
        shutil.copytree(demo_dir, user_demo)

        os.chown(user_dir, uid, gid)
        for root, dirs, files in os.walk(user_dir):
            for walkdir in dirs:
                os.chown(os.path.join(root, walkdir), uid, gid)
            for walkfile in files:
                os.chown(os.path.join(root, walkfile), uid, gid)

        return super().start()


# DockerSpawner options
c.JupyterHub.spawner_class = LocalDockerSpawner
c.DockerSpawner.container_image = 'jupyterhub/singleuser'
c.DockerSpawner.volumes = {
    os.path.join(volume_dir, '{username}'): notebook_dir
}
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.remove_containers = True

# The docker instances need access to the Hub, so the default loopback
# port doesn't work:
docker_ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
c.JupyterHub.hub_ip = docker_ip

c.ConfigurableHTTPProxy.command = [
    'configurable-http-proxy', '--redirect-port', '80']

c.ConfigurableHTTPProxy.api_url = 'http://127.0.0.1:50505'
c.ConfigurableHTTPProxy.auth_token = binascii.b2a_hex(os.urandom(16))

c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True

join = os.path.join
here = os.path.dirname(__file__)
with open(join(here, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

# SSL config
ssl = join(here, 'ssl')
keyfile = join(ssl, 'ssl.key')
certfile = join(ssl, 'ssl.crt')
if os.path.exists(keyfile):
    c.JupyterHub.ssl_key = keyfile
if os.path.exists(certfile):
    c.JupyterHub.ssl_cert = certfile
    c.JupyterHub.port = 443
