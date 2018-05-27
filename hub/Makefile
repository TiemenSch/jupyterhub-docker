start:
	supervisord -c /etc/supervisor/supervisord.conf
	supervisorctl start jupyterhub

restart:
	supervisorctl restart jupyterhub

clean-containers:
	-docker rm -f $(shell docker ps -a | grep 'jupyter-' | awk '{print $$1}')

clean-all: clean-containers
	rm -f jupyterhub_cookie_secret jupyterhub.sqlite
