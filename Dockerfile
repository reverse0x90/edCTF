FROM ubuntu:trusty

# Create environment variables
ENV EDCTF_DIR /opt/edCTF
ENV EDCTF_STATIC_DIR ${EDCTF_DIR}/edctf/static
ENV DJANGO_STATIC_DIR /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static
ENV APACHE_CONFIG /etc/apache2/sites-enabled/000-default.conf
ENV EDCTF_USER edctf

# Install dependancies and intialize
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install apache2 libapache2-mod-wsgi python-pip git \
  && pip install Django djangorestframework markdown django-filter \
  && (wget -qO- https://deb.nodesource.com/setup_4.x | bash) \
  && sudo apt-get install -y nodejs \
  && npm install -g ember-cli \
  && npm install -g bower \
  && mkdir ${EDCTF_DIR} \
  && useradd -m ${EDCTF_USER} \
  && chown ${EDCTF_USER}:${EDCTF_USER} ${EDCTF_DIR}

# Add apache config
ADD apache.conf ${APACHE_CONFIG}

# Switch to EDCTF_USER
USER ${EDCTF_USER}

# add ember and django files
ADD ember ${EDCTF_DIR}/ember
ADD edctf ${EDCTF_DIR}/edctf
ADD manage.py ${EDCTF_DIR}/manage.py

# Install Ember dependancies and move client-side files
RUN cd ${EDCTF_DIR}/ember \
  && npm install \
  && bower install \
  && ember build -prod -o ${EDCTF_STATIC_DIR}/ember \
  && mv ${EDCTF_STATIC_DIR}/ember/index.html ${EDCTF_DIR}/edctf/api/templates/index.html \
  && cp -R ${DJANGO_STATIC_DIR}/admin ${EDCTF_STATIC_DIR}/admin \
  && cp -R /usr/local/lib/python2.7/dist-packages/rest_framework/static/rest_framework ${EDCTF_STATIC_DIR}/rest_framework



USER root
EXPOSE 80 443
CMD /usr/sbin/apache2ctl -D FOREGROUND
