import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
os.chdir(os.getcwd() + '/data')
conn = sqlite3.connect('congress.db')
# congress = pd.read_sql_query("SELECT * FROM congress WHERE congress=114", conn)
congress = pd.read_sql_query("SELECT * FROM congress", conn)
conn.close()

# Make copy of data for working
df = congress.copy()

# Visualize proportion of bills by party
plt.title('Number of bills proposed by party')
plt.xlabel('Sponsor party affiliation')
plt.ylabel('Number of bills proposed')
plt.bar(df['sponsor_party'].value_counts().index.values,
        df['sponsor_party'].value_counts().values)
plt.show();

# Get bill count data
bill_count = df[['sponsor_name', 'congress']].groupby(['sponsor_name']).count()
bill_count.columns = ['num_bills']
bill_count = bill_count.reset_index()
bill_count = bill_count.merge(df[['sponsor_name', 'sponsor_party']], on='sponsor_name').drop_duplicates()
bill_count = bill_count.sort_values(by=['num_bills'], ascending=False)

# Plot the number of bills passed by member, colored by party affiliation
plt.title('Number of bills passed by individual members of house'.title())
plt.xlabel('House Member')
plt.ylabel('Number of bills passed')
plt.scatter(np.arange(bill_count.shape[0]), bill_count['num_bills'],
        color=bill_count['sponsor_party'].map({'R': 'r', 'D': 'b', 'L': 'orange', 'I': 'g'}),
        alpha=0.4)
plt.show();