#!/usr/bin/env python

""" Creates a database """

import sqlite3


print("This version of sqlite3 is %s" % (sqlite3.version))
conn = sqlite3.connect(r"notes_ARGH.db")

cur = conn.cursor()

# Drop it if it already exists
cur.execute("DROP TABLE IF EXISTS stocks")

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS stocks
             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")


stocks = (
    ('2007-01-05','BUY','RHAT',70, 135.14),
    ('2008-01-05','SELL','RHAT',90, 325.10),
    ('2009-01-05','BUY','RHAT',10, 335.13),
    ('2010-01-05','SELL','RHAT',100, 315.14)
)

# Insert using executemany
cur.executemany("INSERT INTO stocks VALUES(?, ?, ?, ?, ?)", stocks)


# Save (commit) the changes
conn.commit()

# Try to get the last transaction row ID
if cur.lastrowid:
    print "Last inserted ID is %d" % (cur.lastrowid)

# Query the DB
cur.execute("SELECT * FROM stocks")
rows = cur.fetchall()
for row in rows:
    print "Row info: ", (row)
    

# Query it a different way
cur.execute("SELECT * FROM stocks")
while True:
    row = cur.fetchone()
    if row == None:
        break
    print row[0], row[1], row[2]
    

# Update a field
cur.execute("UPDATE stocks SET symbol=? WHERE trans=?", (u"GBP", u"SELL"))        
conn.commit()
print "Number of rows updated: %d" % cur.rowcount

# Use a dictionary cursor
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT * FROM stocks")
rows = cur.fetchall()
for row in rows:
    print row.keys()
    print u"%s %s %s %s %s" % (row["date"], row["trans"], row["symbol"], row["qty"], row["price"])  
    
    
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
print "All done!"
