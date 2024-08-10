import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from .models import Exchange

def scrape_boa_and_save_exchange_rates():
    # Send a GET request to the Bank of Abyssinia website
    url = "https://www.bankofabyssinia.com/"
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the exchange rates
    exchange_table = soup.find('table', id='tablepress-15')

    if exchange_table:
        rows = exchange_table.find_all('tr')
        date_str = rows[0].find('th').text.strip()
        
        for row in rows[3:]:  # Start from the 4th row (index 3) to skip headers
            columns = row.find_all('td')
            if len(columns) >= 3:
                currency = columns[0].text.strip()
                buying_rate = columns[1].text.strip()
                selling_rate = columns[2].text.strip()

                try:
                    buying_rate = float(buying_rate)
                    selling_rate = float(selling_rate)
                except ValueError:
                    print(f"Skipping row due to invalid rate: {buying_rate} or {selling_rate}")
                    continue
                
                # Create or update the Exchange object
                Exchange.objects.update_or_create(
                    currency_name=currency,
                    defaults={
                        'buy_rate': buying_rate,
                        'sell_rate': selling_rate,
                        'created_at': timezone.now(),
                        'bank_name': 'Bank of Abyssinia'
                    }
                )
        
        print(f"Exchange rates updated for: {date_str}")
    else:
        print("Exchange rate table not found on the page.")
