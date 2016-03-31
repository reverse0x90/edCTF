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

# Build Django admin css
COPY edctf ${EDCTF}/edctf
RUN cp -R /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin ${EDCTF}/edctf/static/

COPY scripts ${SCRIPTS}

# Build backend
COPY config ${EDCTF}/config
COPY manage.py ${EDCTF}/manage.py
RUN /bin/bash -c ". ${SCRIPTS}/environment.bash \
  && /etc/init.d/postgresql start \
  && ${SCRIPTS}/build_backend.bash \
  && /etc/init.d/postgresql stop"

EXPOSE 80
EXPOSE 443
COPY docker/prod/entrypoint.bash /opt/entrypoint.bash
ENTRYPOINT ["/opt/entrypoint.bash"]
