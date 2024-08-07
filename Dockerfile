# Use an official Python runtime as a parent image
FROM python:3.10

# Install RabbitMQ and its dependencies
RUN apt-get update && apt-get install -y rabbitmq-server

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

# Expose ports
EXPOSE 8000 5672 15672

# Run migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Start RabbitMQ, Celery worker, Celery Beat, and run Django
CMD service rabbitmq-server start && \
    celery -A exchange_dashboard worker --loglevel=info & \
    celery -A exchange_dashboard beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler & \
    python manage.py migrate && \
    gunicorn --bind 0.0.0.0:8000 exchange_dashboard.wsgi:application