import sqlite3
import os
import csv

# Create a connection to the SQLite database - will also crteate the db if not exist
conn = sqlite3.connect('finance_data.db')

cur = conn.cursor()

# Create a finance_data table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS finance_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        date TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        adj_close REAL,
        volume INTEGER,
        CONSTRAINT unique_company_date UNIQUE(company, date)
    )
''')



for filename in os.listdir('data'):
    print("filename")
    if filename.endswith('.csv'):
        company_name = filename[:-4]  # Remove the '.csv' extension from the filename
        filepath = os.path.join('data', filename)
        with open(filepath, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip the header row 
            for row in csvreader:
                print("row")
                date = row[0]
                open_price = float(row[1])
                high_price = float(row[2])
                low_price = float(row[3])
                close_price = float(row[4])
                adj_close_price = float(row[5])
                volume = int(row[6])
                try:
                    cur.execute('''
                        INSERT INTO finance_data (company, date, open, high, low, close, adj_close, volume)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (company_name, date, open_price, high_price, low_price, close_price, adj_close_price, volume))
                except sqlite3.IntegrityError:
                    pass

# Commit
conn.commit()
conn.close()
print("Data added to the Sqlite in the finance_data successfully")
