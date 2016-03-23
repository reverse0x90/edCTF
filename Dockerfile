FROM debian:jessie

ENV EDCTF /opt/edctf
ENV SCRIPTS ${EDCTF}/scripts

# Create directory structure
RUN mkdir ${EDCTF}
COPY . ${EDCTF}
WORKDIR ${EDCTF}

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
RUN pip install -r requirements.txt

# Build frontend css
RUN /bin/bash -c "source ${SCRIPTS}/environment.bash \
  && ${SCRIPTS}/build_frontend-prod.bash"

# Build backend
RUN /bin/bash -c "source ${SCRIPTS}/environment.bash \
  && /etc/init.d/postgresql start \
  && ${SCRIPTS}/build_backend.bash \
  && /etc/init.d/postgresql stop"

EXPOSE 80
EXPOSE 443
ENTRYPOINT ["scripts/start-docker.bash"]
