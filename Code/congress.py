import time
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup


for congress in [113, 114, 115, 116, 117]:
    # Get names of all bills passed in each congress
    congress = str(congress)
    zip_file_name = 'data/BILLSUM-{}-hr.zip'.format(congress)
    with ZipFile(zip_file_name, 'r') as f:
        names = f.namelist()
    
    # Remove all text except for bill number
    bill_ids = [name.replace('.xml','').replace('BILLSUM-{}hr'.format(congress),'')
                for name in names]
    
    # Iterate through all bills for each congress
    for id in bill_ids:
        # Get URL
        url = "https://congress.gov/bill/{}th-congress/house-bill/{}/all-info".format(congress, id)
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