FROM debian:jessie

ENV EDCTF_USER edctf
ENV EDCTF_DIR /opt/edctf

ENV EDCTF_CONFIG  ${EDCTF_DIR}/config
ENV EDCTF_DJANGO  ${EDCTF_DIR}/edctf
ENV EDCTF_EMBER   ${EDCTF_DIR}/ember
ENV EDCTF_SCRIPTS ${EDCTF_DIR}/scripts

# Install packages
RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive \
    apt-get -y install \
        apache2 \
        libapache2-mod-wsgi \
        libpq-dev \
        postgresql=9.4* \
        python-pip \
        python-dev \
        sudo \
        openssl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY scripts/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Create directory structure
RUN mkdir ${EDCTF_DIR} \
  && mkdir ${EDCTF_SCRIPTS}

# Add environment variables script
COPY scripts/environment.bash ${EDCTF_SCRIPTS}/environment.bash

#Copy Django base
COPY edctf ${EDCTF_DJANGO}

# Copy frontend
COPY scripts/build_frontend-prod.bash ${EDCTF_SCRIPTS}/build_frontend-prod.bash

# Build frontend css
RUN /bin/bash -c "source ${EDCTF_SCRIPTS}/environment.bash \
  && ${EDCTF_SCRIPTS}/build_frontend-prod.bash"

# Copy backend
COPY manage.py ${EDCTF_DIR}/manage.py
COPY config ${EDCTF_CONFIG}
COPY scripts/generate_secrets.py ${EDCTF_SCRIPTS}/generate_secrets.py
COPY scripts/build_backend.bash ${EDCTF_SCRIPTS}/build_backend.bash

# Build backend
RUN /bin/bash -c "source ${EDCTF_SCRIPTS}/environment.bash \
  && /etc/init.d/postgresql start \
  && ${EDCTF_SCRIPTS}/build_backend.bash \
  && /etc/init.d/postgresql stop"

# Add container start script
COPY scripts/start-docker.bash ${EDCTF_SCRIPTS}/start-docker.bash

WORKDIR ${EDCTF_DIR}
EXPOSE 80
EXPOSE 443
ENTRYPOINT ["scripts/start-docker.bash"]
