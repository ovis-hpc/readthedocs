FROM fluxrm/flux-sched:focal

# Match the default user id for a single system so we aren't root
ARG USERNAME=spwalto
ARG USER_UID=1000
ARG USER_GID=1000
ENV USERNAME=${USERNAME}
ENV USER_UID=${USER_UID}
ENV USER_GID=${USER_GID}

LABEL maintainer="spwalto <@spwalto>"

# Pip not provided in this version
USER root

RUN apt-get update && apt-get install -y iputils-ping python3.9-venv python3.9-dev \
    ca-certificates curl && apt-get clean
COPY ./requirements.txt /requirements.txt 
COPY ./.github/dev-requirements.txt /dev-requirements.txt
COPY certs/ /etc/ssl/certs

ENV PYTHONPATH=/usr/lib/python3.9

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# For easier Python development.
RUN python3.9 -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org IPython && \
    python3.9 -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r /requirements.txt && \
    python3.9 -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r /dev-requirements.txt && \
    python3.9 -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org sphinx sphinx-rtd-theme && \
    python3.9 -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org pymdown-extensions && \
    # For developer convenience
    ln -s /usr/bin/python3.9 /usr/bin/python

# Add the group and user that match our ids
RUN groupadd -g ${USER_GID} ${USERNAME} && \
    adduser --disabled-password --uid ${USER_UID} --gid ${USER_GID} --gecos "" ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers && \
    echo "root ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN chown root:${USERNAME} /bin/bash
RUN chmod 755 /bin/bash

# Configure global inputrc to bind Page Up/Down for history search
RUN echo '"\e[5~": history-search-backward\n\
"\e[6~": history-search-forward' > /etc/inputrc

# Set the environment variable so bash always uses /etc/inputrc
ENV INPUTRC=/etc/inputrc

USER $USERNAME

ENV PATH=/env/bin:${PATH}
WORKDIR /workspace/ovis-docs
