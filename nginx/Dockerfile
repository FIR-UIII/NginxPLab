FROM nginx:1.20-alpine

# Add bash for boot cmd
RUN apk add bash

# Override the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /home/web/default