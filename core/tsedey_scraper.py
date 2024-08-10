import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from django.utils import timezone
from .models import Exchange  

def scrape_tsedey_and_save_exchange_rates():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, we're mimicing a browser
    url = "https://tsedeybank-sc.com/"
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with the exchange rates
    table = soup.find('table', class_='wptb-preview-table')

    if table:
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 3:
                currency_div = cells[0].find('div', id='exchange')
                if currency_div:
                    currency_code = currency_div.find('h4').text.strip()
                    currency_name = currency_div.find('span').text.strip()
                    buying_rate = Decimal(cells[1].text.strip())
                    selling_rate = Decimal(cells[2].text.strip())

                    # Create or update Exchange objects
                    Exchange.objects.update_or_create(
                        currency_name=currency_code,
                        bank_name="Tsedey Bank",
                        defaults={
                            'buy_rate': buying_rate,
                            'sell_rate': selling_rate,
                            'updated_at': timezone.now()
                        }
                    )

        print("Exchange rates updated successfully.")
    else:
        print("Exchange rate table not found on the page.")


