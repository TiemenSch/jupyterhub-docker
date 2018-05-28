# JupyterHub

Docker image with the goal of spawning a JupyterHub Docker container alongside singleuser notebook containers.

It should do so by controlling its parent docker daemon by running:

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock -ti jupyterhub-docker:latest
```

Currently in an unfinished state.

See https://github.com/TiemenSch/tiniconda/tree/master/util for the helper commands used in the image.
