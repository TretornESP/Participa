FROM nginx:1.23.3

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY server.conf /etc/nginx/conf.d/
COPY nginx-certificate.crt /etc/nginx/certificate/nginx-certificate.crt
COPY nginx.key /etc/nginx/certificate/nginx.key