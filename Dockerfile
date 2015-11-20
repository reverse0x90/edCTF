# This is currently a temporary solution
FROM ubuntu:trusty

ENV DEBIAN_FRONTEND noninteractive

# Set directory paths
ENV EDCTF_DIR /opt/edctf
ENV EDCTF_STATIC ${EDCTF_DIR}/edctf/static
ENV EDCTF_DJANGO_STATIC /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static
ENV EDCTF_REST_STATIC /usr/local/lib/python2.7/dist-packages/rest_framework/static/rest_framework/
ENV EDCTF_APACHE_CONFIG /etc/apache2/sites-enabled/000-default.conf

# Set user
ENV EDCTF_USER edctf

# Create project directory
RUN mkdir ${EDCTF_DIR}

# Set work directory
WORKDIR ${EDCTF_DIR}

# Add requirements.txt
ADD requirements.txt requirements.txt

# Install dependancies
RUN apt-get clean \
  && apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install wget apache2 libapache2-mod-wsgi python-pip python-dev git postgresql-9.3 libpq-dev \
  && pip install -r requirements.txt \
  && (wget -qO- https://deb.nodesource.com/setup_4.x | bash) \
  && apt-get install -y nodejs \
  && npm install -g ember-cli \
  && npm install -g bower

# Add apache config
ADD apache.conf ${EDCTF_APACHE_CONFIG}

# Add Ember and Django files
ADD ember ember
ADD edctf edctf
ADD manage.py manage.py
ADD generate_secrets.py generate_secrets.py
ADD createsuperuser.py createsuperuser.py

# Set ownership
RUN useradd -m ${EDCTF_USER} \
  && chown ${EDCTF_USER}:${EDCTF_USER} -R ${EDCTF_DIR} \
  && chmod 775 -R ${EDCTF_DIR}

# Switch to EDCTF_USER
USER ${EDCTF_USER}

# Install Ember dependancies and build
RUN cd ember \
  && git config --global url."https://".insteadOf git:// \
  && npm install \
  && bower install -q

# Create static files
RUN cd ember \
  && ember build -prod -o ${EDCTF_STATIC}/ember \
  && cp -R ${EDCTF_DJANGO_STATIC}/admin/ ${EDCTF_STATIC}/admin \
  && cp -R ${EDCTF_REST_STATIC} ${EDCTF_STATIC}/rest_framework

# Change back to root
USER root

# Initialize edctf database
RUN /etc/init.d/postgresql start \
  && python generate_secrets.py \
  && python manage.py makemigrations \
  && python manage.py migrate \
  && cat createsuperuser.py | python manage.py shell

EXPOSE 80

CMD (sudo -u postgres /usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main -c config_file=/etc/postgresql/9.3/main/postgresql.conf &) \
  && /usr/sbin/apache2ctl restart \
  && tail -f /dev/null
