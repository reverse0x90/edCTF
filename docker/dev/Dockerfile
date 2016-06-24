FROM debian:jessie

ENV EDCTF /opt/edctf
ENV SCRIPTS "${EDCTF}/scripts"

# Create directory structure
RUN mkdir "${EDCTF}"
WORKDIR "${EDCTF}"

# Install packages
RUN apt-get clean \
  && apt-get update \
  && DEBIAN_FRONTEND=noninteractive \
    apt-get -y install \
        apache2 \
        curl \
        libapache2-mod-wsgi \
        libpq-dev \
        git \
        netcat \
        npm \
        openssl \
        python-pip \
        python-dev \
        sudo

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Update npm
RUN npm install -g n \
  && n 0.12.12

# Install ember and bower
RUN npm install -g ember-cli
RUN npm install -g bower

COPY scripts "${SCRIPTS}"
COPY ember ember
COPY edctf edctf
COPY config config
COPY manage.py manage.py

COPY docker docker
RUN cp "${EDCTF}/docker/dev/entrypoint.bash" /opt/entrypoint.bash

EXPOSE 80
EXPOSE 443
ENTRYPOINT ["/opt/entrypoint.bash"]
