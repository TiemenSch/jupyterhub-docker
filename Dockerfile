FROM tiemensch/tiniconda:alpine-3.7

USER root

RUN min-apk docker make

USER $NB_USER
RUN min-conda git jupyterhub netifaces && \
    cd $HOME && \
    pip install git+https://github.com/Supervisor/supervisor.git#egg=supervisor && \
    pip install git+https://github.com/jupyter/oauthenticator#egg=oauthenticator && \
    pip install git+https://github.com/jupyter/dockerspawner#egg=dockerspawner && \
    clean-conda && \
    fix-permissions $CONDA_DIR $HOME

USER root

COPY /jupyterhub.conf /etc/supervisor/conf.d/jupyterhub.conf
COPY /supervisord.conf /etc/supervisor/supervisord.conf
COPY /hub /srv/jupyterhub
RUN  mkdir -p /mnt/work/jupyterhub
RUN fix-permissions /srv/jupyterhub /mnt/work/jupyterhub

USER $NB_USER

WORKDIR /srv/jupyterhub
