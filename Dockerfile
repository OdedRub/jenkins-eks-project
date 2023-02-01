FROM nginx
RUN mkdir /etc/nginx/certificate
COPY ./certificates/* /etc/nginx/certificate/
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./index.html /usr/share/nginx/html/index.html
