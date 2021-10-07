import os
import sqlite3
import time
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup
from requests.api import get

# from Code.database_creation import insert_data

# Change directory
os.chdir(os.getcwd() + '/data')


def get_bill_ids(congress_yr):
    """Returns a list of all the measure-numbers (ids) from a given congress. 
    Data should be stored as an unedited zip file as found on 
    https://www.govinfo.gov/bulkdata/BILLSUM

    Arguments
    congress_yr : Congressional year either 113-117
    """
    congress_yr = str(congress_yr)
    zip_file_name = 'BILLSUM-{}-hr.zip'.format(congress_yr)
    with ZipFile(zip_file_name, 'r') as f:
        names = f.namelist()

    # Remove all text except for bill number
    bill_ids = [name.replace('.xml','').replace(
                'BILLSUM-{}hr'.format(congress_yr),'') for name in names]
    return bill_ids


def scrape_congress(congress_yr, bill_ids, db_name):
    """Scrapes bill summary data from congress.gov. Exctracts the sponsor's 
    name, sponsor's party, bill name, and bill summary. 
    
    Arguments
    congress_yr : Congressional year either 113-117
    bill_ids : The measure number of a bill
    db_name : Name of database to store the data
    """
    # Initialize database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Iterate through all bills for each congress
    for id in bill_ids:
        # Format URL
        url = ("https://congress.gov/bill/{}th-congress"
               "/house-bill/{}/all-info").format(congress_yr, id)

        # Request page
        page = requests.get(url)

        # Make sure page exists
        if page.status_code == 200:
            # Parse page contents
            soup = BeautifulSoup(page.content, 'html.parser')

            # Get sponsor info
            sponsor_data = soup.find('tr').get_text().strip('\n').split('.')
            sponsor_name = "".join(sponsor_data[1].strip().split(','))
            sponsor_party = sponsor_data[-1].strip()[1]

            # Get bill info
            bill_summary_data = soup.find('div', 
                                          id='bill-summary').find_all('p')
            bill_summary = []
            for idx, p in enumerate(bill_summary_data):
                if idx == 0:
                    bill_name = p.get_text()
                else:
                    bill_summary.append(p.get_text())

            # Convert bill summary to single string
            bill_summary = "".join(bill_summary)
                        
            data = (congress_yr, id, sponsor_name, sponsor_party, 
                    bill_name, bill_summary)
            
            # Get table name from database
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table = c.fetchall()[0][0]

            # Insert data into database
            with conn:
                c.execute(f"INSERT INTO {table} VALUES (?,?,?,?,?,?)", data)

            # Don't strain the servers
            time.sleep(3)
        else:
            time.sleep(3)
            continue
    
    # Close connection to database
    conn.close()


# CHECK CODE
# bill_ids = [1]
# scrape_congress(117, bill_ids, 'congress.db')

# conn = sqlite3.connect('congress.db')
# c = conn.cursor()
# c.execute("SELECT * FROM congress")
# c.fetchall()
# c.execute("DELETE FROM congress WHERE id = (SELECT MAX(id) FROM congress)")
# conn.commit()
# conn.close()


# ESTIMATED RUN TIME: 44.53 HOURS
# num_bills = sum([len(get_bill_ids(113)), len(get_bill_ids(114)),
#                  len(get_bill_ids(115)), len(get_bill_ids(116)),
#                  len(get_bill_ids(117))])
                       
# single_iteration = 5  # seconds
# print(f"Estimated run time is {round(num_bills*single_iteration/3600,2)} hours")


# Iterate through each congress
# for congress in [113, 114, 115, 116, 117]:
#     bill_ids = get_bill_ids(congress)
#     scrape_congress(congress, bill_ids, 'congress.db')

