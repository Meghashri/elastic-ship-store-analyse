FROM php:7.2-apache
#COPY apache2.conf /etc/apache2/apache2.conf

COPY sites-available/* /etc/apache2/sites-available/

RUN /usr/sbin/a2enmod \
    headers \
    proxy \
    proxy_http \
    ssl \
    && htpasswd -cb /etc/apache2/.htpasswd "someone" "someonetrial" 

EXPOSE 443
EXPOSE 80

RUN /usr/sbin/a2ensite someone_kibana
RUN /usr/sbin/a2ensite someone_elastics

CMD ["apache2ctl", "-D", "FOREGROUND"]
