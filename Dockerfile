FROM debian:jessie

ENV EDCTF_USER edctf
ENV EDCTF_DIR /opt/edctf

ENV EDCTF_CONFIG  ${EDCTF_DIR}/config
ENV EDCTF_DJANGO  ${EDCTF_DIR}/edctf
ENV EDCTF_EMBER   ${EDCTF_DIR}/ember
ENV EDCTF_SCRIPTS ${EDCTF_DIR}/scripts

# Install packages
RUN apt-get update \
  && apt-get -y install \
    apache2 \
    curl \
    git \
    libapache2-mod-wsgi \
    libpq-dev \
    postgresql=9.4* \
    python-pip \
    python-dev \
    sudo \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python and Javascript dependencies
COPY scripts/requirements.txt requirements.txt
RUN pip install -r requirements.txt \
  && (curl -sL https://deb.nodesource.com/setup | bash -) \
  && DEBIAN_FRONTEND=noninteractive \
    apt-get install -y nodejs \
  && npm install -g ember-cli \
  && npm install -g bower \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir ${EDCTF_DIR} \
  && mkdir ${EDCTF_SCRIPTS}

# Add non-root user for ember dependencies
RUN useradd -m ${EDCTF_USER} \
  && echo "${EDCTF_USER} ALL = (ALL) NOPASSWD: ALL" > /etc/sudoers.d/${EDCTF_USER}

# Add environment variables script
COPY scripts/environment.bash ${EDCTF_SCRIPTS}/environment.bash

# Copy frontend
COPY ember ${EDCTF_EMBER}
COPY scripts/build_frontend.bash ${EDCTF_SCRIPTS}/build_frontend.bash

# Change permissions
RUN chown -R ${EDCTF_USER}:${EDCTF_USER} ${EDCTF_DIR}

# Switch to non-root for ember
USER ${EDCTF_USER}

# Build frontend
RUN /bin/bash -c "source ${EDCTF_SCRIPTS}/environment.bash \
  && git config --global url.'https://'.insteadOf git:// \
  && ${EDCTF_SCRIPTS}/build_frontend.bash"

# Copy backend
COPY manage.py ${EDCTF_DIR}/manage.py
COPY edctf ${EDCTF_DJANGO}
COPY config ${EDCTF_CONFIG}
COPY scripts/generate_secrets.py ${EDCTF_SCRIPTS}/generate_secrets.py
COPY scripts/build_backend.bash ${EDCTF_SCRIPTS}/build_backend.bash

# Add container start script
COPY scripts/start-docker.bash ${EDCTF_SCRIPTS}/start-docker.bash

USER root

# Change permissions
RUN chown -R ${EDCTF_USER}:${EDCTF_USER} \
  ${EDCTF_DIR}/manage.py \
  ${EDCTF_DJANGO} \
  ${EDCTF_CONFIG} \
  ${EDCTF_SCRIPTS}/generate_secrets.py \
  ${EDCTF_SCRIPTS}/build_backend.bash

# Build backend
RUN /bin/bash -c "source ${EDCTF_SCRIPTS}/environment.bash \
  && /etc/init.d/postgresql start \
  && ${EDCTF_SCRIPTS}/build_backend.bash \
  && /etc/init.d/postgresql stop"

WORKDIR ${EDCTF_DIR}
EXPOSE 80
ENTRYPOINT ["scripts/start-docker.bash"]
