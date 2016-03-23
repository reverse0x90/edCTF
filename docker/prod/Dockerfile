FROM debian:jessie

ENV EDCTF /opt/edctf
ENV SCRIPTS ${EDCTF}/scripts

# Create directory structure
RUN mkdir ${EDCTF}
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
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY scripts ${SCRIPTS}

# Build frontend css
COPY edctf edctf
RUN /bin/bash -c ". ${SCRIPTS}/environment.bash \
  && ${SCRIPTS}/build_frontend-prod.bash"

# Build backend
COPY config config
COPY manage.py manage.py
RUN /bin/bash -c ". ${SCRIPTS}/environment.bash \
  && /etc/init.d/postgresql start \
  && ${SCRIPTS}/build_backend.bash \
  && /etc/init.d/postgresql stop"

COPY docker docker
RUN cp ${EDCTF}/docker/prod/entrypoint.bash /opt/entrypoint.bash

EXPOSE 80
EXPOSE 443
ENTRYPOINT ["/opt/entrypoint.bash"]
