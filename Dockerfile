FROM docker:latest

# Install Redis
RUN apt-get update && apt-get install -y redis-server

# Install RabbitMQ
RUN apt-get update && apt-get install -y rabbitmq-server

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Expose Redis, RabbitMQ, and Nginx ports
EXPOSE 6379 5672 80

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Set up the Redis data volume
VOLUME /data

# Start Redis, RabbitMQ, and Nginx services
CMD service redis-server --appendonly yes start && service rabbitmq-server start && nginx -g 'daemon off;'