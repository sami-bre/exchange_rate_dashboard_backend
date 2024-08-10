# Use an official Python runtime as a parent image
FROM python:3.10

# Install RabbitMQ and its dependencies
RUN apt-get update && apt-get install -y rabbitmq-server

# Install PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Create a PostgreSQL user and database
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER django WITH SUPERUSER PASSWORD 'django';" && \
    createdb -O django exchange_dashboard
USER root

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Create a script to wait for PostgreSQL and start the application
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
until PGPASSWORD=django psql -h "localhost" -U "django" -d "exchange_dashboard" -c "\q"; do\n\
  >&2 echo "PostgreSQL is unavailable - sleeping"\n\
  sleep 1\n\
done\n\
\n\
>&2 echo "PostgreSQL is up - executing command"\n\
\n\
python manage.py migrate\n\
celery -A exchange_dashboard worker --loglevel=info & \n\
celery -A exchange_dashboard beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler & \n\
gunicorn --bind 0.0.0.0:8000 exchange_dashboard.wsgi:application\n\
' > /code/start.sh

RUN chmod +x /code/start.sh

# Expose ports
EXPOSE 8000 5672 15672

# Start Postgre, RabbitMQ, and run the start script
CMD service postgresql start && \
    service rabbitmq-server start && \
    /code/start.sh