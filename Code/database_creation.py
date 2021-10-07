import sqlite3


def initailize_db(db_name):
    """Create a database called congress that has four columns 
    sponsor_name
    sponsor_party
    bill_name
    bill_party
    """
    # Create database
    conn = sqlite3.connect(db_name)

    # Create cursor
    c = conn.cursor()

    # Create table and columns: txt and action
    c.execute(
        """CREATE TABLE congress (
                congress text,
                hr_measure text,
                sponsor_name text,
                sponsor_party text,
                bill_name text,
                bill_summary text
                )"""
    )

    # Commit table
    conn.commit()

    # Close database
    conn.close()


def insert_data(db_name, data):
    """Insert values of data into database.
    
    Arguments
    db_name : Name of database
    data : A tuple (sponsor_name, sponsor_party, bill_name, bill_party)
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO congress VALUES (?,?,?,?)", data)
    conn.close()


def db_head(db_name, n):
    """Print the first n rows of a database."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print(c.execute("SELECT * FROM training_data").fetchmany(n))
    conn.close()


# Initialize db
# initailize_db("congress.db")

# Insert messages
# insert_data("congress.db", data)

# Preview first 5 rows
# db_head("congress.db", 5)
