import time
import requests
from bs4 import BeautifulSoup

for bill_number in range(10_000):
    # Get URL
    url = "https://congress.gov/bill/117th-congress/house-bill/{}/all-info".format(bill_number)
    page = requests.get(url)

    # Make sure page exists
    if page.status_code == 200:
        # Parse page contents
        soup = BeautifulSoup(page.content, 'html.parser')

        # Get sponsor info
        sponsor_info = soup.find('tr').get_text().strip('\n').split('.')
        sponsor_name = sponsor_info[1].strip()
        sponsor_party = sponsor_info[-1].strip()[1]

        # Get bill info
        bill_summary_info = soup.find('div', id='bill-summary').find_all('p')
        bill_summary = []
        for idx, p in enumerate(bill_summary_info):
            if idx == 0:
                bill_name = p.get_text()
            else:
                bill_summary.append(p.get_text())

        # Add data to database
        # INSERT CODE HERE
        data = [sponsor_name, sponsor_party, bill_name, bill_summary]
        # c.execute("INSERT INTO bills (?,?)", )

        time.sleep(3)
    else:
        time.sleep(3)
        continue