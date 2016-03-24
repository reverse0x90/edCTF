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
        curl \
        libapache2-mod-wsgi \
        libpq-dev \
        git \
        npm \
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

# Update npm
RUN npm install -g n \
  && n 0.12.12

# Install ember and bower
RUN npm install -g ember-cli
RUN npm install -g bower

COPY scripts ${SCRIPTS}

# Build frontend css
COPY ember ember
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
RUN cp ${EDCTF}/docker/dev/entrypoint.bash /opt/entrypoint.bash

EXPOSE 80
EXPOSE 443
ENTRYPOINT ["/opt/entrypoint.bash"]
