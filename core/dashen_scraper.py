import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from django.utils import timezone
from .models import Exchange

def scrape_dashen_and_save_exchange_rates():
    url = "https://dashenbanksc.com/daily-exchange-rates/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the exchange rate tables
    container = soup.find('div', class_='exchangeratetable')
    table = container.find('table') if container else None

    if table:
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 4:
                currency_code = columns[0].text.strip().split()[-1]
                currency_name = columns[1].text.strip()
                buying_rate = Decimal(columns[2].text.strip())
                selling_rate = Decimal(columns[3].text.strip())
                
                # Create new Exchange object
                Exchange.objects.create(
                    currency_name=currency_code,
                    bank_name="Dashen Bank",
                    buy_rate=buying_rate,
                    sell_rate=selling_rate,
                    updated_at=timezone.now()
                )
        print("New exchange rates created successfully.")
    else:
        print("Exchange rate table not found on the page.")