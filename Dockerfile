FROM ubuntu:trusty

# Set directory paths
ENV EDCTF_DIR /opt/edctf
ENV EDCTF_STATIC ${EDCTF_DIR}/edctf/static
ENV EDCTF_DJANGO_STATIC /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static
ENV EDCTF_REST_STATIC /usr/local/lib/python2.7/dist-packages/rest_framework/static/rest_framework/
ENV EDCTF_APACHE_CONFIG /etc/apache2/sites-enabled/000-default.conf

# Set users
ENV EDCTF_USER edctf
ENV EDCTF_WWW_GROUP www-data

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
  && chown ${EDCTF_USER}:${EDCTF_WWW_GROUP} ${EDCTF_DIR}

# Add apache config
ADD apache.conf ${EDCTF_APACHE_CONFIG}

# Switch to EDCTF_USER
USER ${EDCTF_USER}

# Add Ember and Django files
ADD ember ${EDCTF_DIR}/ember
ADD edctf ${EDCTF_DIR}/edctf
ADD manage.py ${EDCTF_DIR}/manage.py

# Install Ember dependancies and move client-side files
RUN cd ${EDCTF_DIR}/ember \
  && npm install \
  && bower install \
  && ember build -prod -o ${EDCTF_STATIC}/ember \
  && mv ${EDCTF_STATIC}/ember/index.html ${EDCTF_DIR}/edctf/api/templates/index.html \
  && mv ${EDCTF_STATIC}/ember/robots.txt ${EDCTF_DIR}/edctf/api/templates/robots.txt \
  && mv ${EDCTF_STATIC}/ember/crossdomain.xml ${EDCTF_DIR}/edctf/api/templates/crossdomain.xml \
  && cp -R ${EDCTF_DJANGO_STATIC}/admin/ ${EDCTF_STATIC}/admin \
  && cp -R ${EDCTF_REST_STATIC} ${EDCTF_STATIC}/rest_framework

# Initialize Django database
RUN cd ${EDCTF_DIR} \
  && python manage.py makemigrations \
  && python manage.py migrate \
  && python manage.py createsuperuser

# Allow apache access
USER root
RUN sudo chown ${EDCTF_USER}:${EDCTF_WWW_GROUP} ${EDCTF_DIR} \
  && sudo chmod +w ${EDCTF_DIR} \
  && sudo chown ${EDCTF_USER}:${EDCTF_WWW_GROUP} ${EDCTF_DIR}/*.sqlite3 \
  && sudo chmod +w ${EDCTF_DIR}/*.sqlite3

EXPOSE 80 443
CMD /usr/sbin/apache2ctl -D FOREGROUND
