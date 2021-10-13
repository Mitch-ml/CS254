import os
import sqlite3
import time
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup

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
    bill_ids = [int(name) for name in bill_ids]
    return sorted(bill_ids)


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

            # Handle sponsor's name
            try:
                sponsor_name = ("".join(sponsor_data[1].strip().split(','))
                                .split('[')[0].strip())
            # Handle sponspr's middle name 
            except IndexError:
                try:
                    sponsor_name = ("".join(sponsor_data[1].strip().split(',')))
                # Handle special names (i.e. commissioner)
                except IndexError:
                    sponsor_name = "".join(sponsor_data).strip().split('[')[0].split('\n')[-1].strip()
            
            sponsor_party = "".join(sponsor_data[-1]).split('[')[1][0]

            # Get bill info (find all paragraphs)
            bill_summary_data = soup.find('div', 
                                          id='bill-summary').find_all('p')
            
            # If bill_summary_data is not empty extract the bill name and summary
            if bill_summary_data != []:
                try:
                    # See if bill name is in bold
                    bill_name = [title.get_text() for title in soup.find('div', id='bill-summary').find_all('b')][0]
                except IndexError:
                    try:
                        # See if bill name is strong instead of bold 
                        bill_name = [title.get_text() for title in soup.find('div', id='bill-summary').find_all('strong')][0]
                    except IndexError:
                        # No bill name present
                        pass

                # Get bill summary
                bill_summary = [p.get_text() for p in soup.find('div', id='bill-summary').find_all('p')]

                # If bill name is not empty remove duplicate value in bill summary
                if bill_name in bill_summary:
                    del bill_summary[0]
                    bill_summary = "".join(bill_summary)
                else:
                    bill_name = None
                    bill_summary = "".join(bill_summary)
            
            # If there are no paragraphs look for text after headers
            else:
                bill_name = None
                bill_summary = soup.find('div', id='bill-summary').findChildren(text=True)[-1]
                bill_summary = "".join(bill_summary)
                # bill_summary = soup.find('div', id='bill-summary').find('h3', class_='currentVersion').findNextSibling(text=True)

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


# conn = sqlite3.connect('congress.db')
# c = conn.cursor()
# c.execute("SELECT * FROM congress")
# c.fetchall()
# conn.close()

# ESTIMATED RUN TIME: 44.53 HOURS
# num_bills = sum([len(get_bill_ids(113)), len(get_bill_ids(114)),
#                  len(get_bill_ids(115)), len(get_bill_ids(116)),
#                  len(get_bill_ids(117))])
                       
# Iterate through each congress
# for congress in [113, 114, 115, 116]:
#     bill_ids = get_bill_ids(congress)
#     scrape_congress(congress, bill_ids, 'congress.db')

CONGRESS_YR = 116
bill_ids = get_bill_ids(CONGRESS_YR)
scrape_congress(CONGRESS_YR, bill_ids, 'congress.db') 
# start time: 10:24 (116)
# Estimated finish 22:24
# Actual Finish time: 20:36

# conn = sqlite3.connect('congress.db')
# df = pd.read_sql_query("SELECT * from congress", conn)
# conn.close()
# df.tail()
# bill_ids[:100]
# df['sponsor_party'].value_counts()