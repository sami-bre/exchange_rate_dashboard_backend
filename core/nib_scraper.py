import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from django.utils import timezone
from core.models import Exchange  # Import the Exchange model

def scrape_nib_and_save_exchange_rates():
    url = "https://www.nibbanksc.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    exchange_tables = soup.find_all('table', class_='ea-advanced-data-table')

    if len(exchange_tables) >= 2:
        exchange_table = exchange_tables[1]  # Use the second table
        rows = exchange_table.find_all('tr')

        # Skip the header row
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 6:
                currency = cols[1].text.strip()
                cash_buying = Decimal(cols[2].text.strip())
                cash_selling = Decimal(cols[3].text.strip())
                trans_buying = Decimal(cols[4].text.strip())
                trans_selling = Decimal(cols[5].text.strip())

                # Create or update Exchange objects for cash rates
                Exchange.objects.update_or_create(
                    currency_name=currency,
                    bank_name="NIB Bank Cash",
                    defaults={
                        'buy_rate': cash_buying,
                        'sell_rate': cash_selling,
                        'updated_at': timezone.now()
                    }
                )

                # Create or update Exchange objects for transactional rates
                Exchange.objects.update_or_create(
                    currency_name=currency,
                    bank_name="NIB Bank",
                    defaults={
                        'buy_rate': trans_buying,
                        'sell_rate': trans_selling,
                        'updated_at': timezone.now()
                    }
                )

        print("Exchange rates updated successfully.")
    else:
        print("Exchange rate table not found on the page.")