from celery import shared_task
from core.berhan_scraper import scrape_berhan_and_save_exchange_rates
from core.boa_scraper import scrape_boa_and_save_exchange_rates
from core.nib_scraper import scrape_nib_and_save_exchange_rates
from core.tsedey_scraper import scrape_tsedey_and_save_exchange_rates
from core.dashen_scraper import scrape_dashen_and_save_exchange_rates


@shared_task
def scrape_boa():
    scrape_boa_and_save_exchange_rates()
    return "Scraping BOA completed"


@shared_task
def scrape_nib():
    scrape_nib_and_save_exchange_rates()
    return "Scraping NIB completed"


@shared_task
def scrape_tsedey():
    scrape_tsedey_and_save_exchange_rates()
    return "Scraping Tsedey completed"


@shared_task
def scrape_berhan():
    scrape_berhan_and_save_exchange_rates()
    return "Scraping Berhan completed"


@shared_task
def scrape_dashen():
    scrape_dashen_and_save_exchange_rates()
    return "Scraping Dashen completed"