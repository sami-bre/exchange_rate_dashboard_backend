# Bank of Abyssinia Exchange Rate Scraper

This project is a Django-based web scraper that automatically fetches and stores exchange rates from the Bank of Abyssinia website. It uses Celery for task scheduling and Docker for easy deployment and management.

## Features

- Scrapes exchange rates from the Bank of Abyssinia website
- Stores the data in a database using Django models
- Automatically updates exchange rates every 2 minutes using Celery
- Dockerized for easy setup and deployment

## Prerequisites

- Docker
- Docker Compose

## Setup and Running

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Build and run the Docker container:
   ```
   sudo docker build -t exchange_dashboard .
   sudo docker run -p 8000:8000 -p 5672:5672 -p 15672:15672 exchange_dashboard
   ```

   This command will:
   - Build the Docker image for the Django application
   - Start the container, which includes:
     - The Django web server
     - The Celery worker
     - The Celery beat scheduler

3. The application should now be running. You can access the Django REST Framework API documentation at `http://localhost:8000/api` to view and interact with the scraped exchange rates.

## Project Structure

- `core/`: The main Django app containing the scraper logic
  - `boa_scrapper.py`: Contains the scraping function
  - `models.py`: Defines the Exchange model for storing rate data
  - `tasks.py`: Defines the Celery task for running the scraper
  - `scheduling.py`: Sets up the periodic task for Celery
- `Dockerfile`: Defines the Docker image for the application
- `docker-compose.yml`: Orchestrates the different services (web, celery, database)

## Customization

- To change the scraping interval, modify the `every` parameter in `core/scheduling.py`
- To add more banks or currencies, extend the `scrape_boa_and_save_exchange_rates` function in `core/boa_scrapper.py`

## Troubleshooting

If you encounter any issues, check the Docker logs.
