FROM ubuntu:trusty

# Create environment variables
ENV EDCTF_DIR /opt/edctf
ENV EDCTF_STATIC_DIR ${EDCTF_DIR}/edctf/static
ENV DJANGO_STATIC_DIR /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static
${EDCTF_STATIC_DIR}

# Install dependancies and intialize
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install apache2 libapache2-mod-wsgi python-pip git \
  && pip install Django djangorestframework markdown django-filter \
  && mkdir ${EDCTF_DIR} \
  && useradd -m edctf \
  && chown edctf:edctf ${EDCTF_DIR}

# Add apache config
ADD apache.conf /etc/apache2/sites-enabled/000-default.conf

# Switch to edctf user
USER edctf

# add ember and django files
ADD ember ${EDCTF_DIR}/ember
ADD edctf ${EDCTF_DIR}/edctf
ADD manage.py ${EDCTF_DIR}/manage.py

# Install Ember dependancies and move client-side files
RUN wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.29.0/install.sh | bash
RUN nvm install v4.1.2 \
  && nvm alias default v4.1.2 \
  && npm install -g ember-cli \
  && npm install -g bower \
  && cd ${EDCTF_DIR}/ember \
  && npm install \
  && bower install \
  && ember build -prod -o ${EDCTF_STATIC_DIR}/ember \
  && mv ${EDCTF_STATIC_DIR}/ember/index.html ${EDCTF_DIR}/edctf/api/templates/index.html \
  && cp -R ${DJANGO_STATIC_DIR}/admin/* ${EDCTF_STATIC_DIR}/admin/.



USER root
EXPOSE 80 443
CMD /usr/sbin/apache2ctl -D FOREGROUND
