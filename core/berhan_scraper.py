import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from django.utils import timezone
from .models import Exchange

def scrape_berhan_and_save_exchange_rates():
    url = "https://berhanbanksc.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the container with exchange rates
    container = soup.find('div', class_='tableContainer')

    if container:
        rows = container.find_all('div', class_='row customRow mb-2')
        for row in rows:
            currency_info = row.find('div', class_='col-6')
            currency_code = currency_info.find('input')['id']
            currency_name = currency_info.find('span', string=lambda text: text and len(text.strip()) > 0).text.strip()
            
            buying_rate = Decimal(row.find_all('div', class_='col-3')[0].text.strip())
            selling_rate = Decimal(row.find_all('div', class_='col-3')[1].text.strip())

            # Create new Exchange objects
            Exchange.objects.create(
                currency_name=currency_code,
                bank_name="Berhan Bank",
                buy_rate=buying_rate,
                sell_rate=selling_rate,
                updated_at=timezone.now()
            )
        print("New exchange rates created successfully.")
    else:
        print("Exchange rate container not found on the page.")