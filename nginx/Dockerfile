FROM nginx:1.20-alpine

# Add bash for boot cmd
RUN apk add bash

# Add nginx.conf to container
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN mkdir -p /home/web/default