from celery import shared_task

from core.boa_scrapper import scrape_boa_and_save_exchange_rates

@shared_task
def scrape_boa():
    scrape_boa_and_save_exchange_rates()
    return "Scraping BOA completed"