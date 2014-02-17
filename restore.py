#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Restore database from file """

import sqlite3 as lite
import sys

def readData():
    """ Read the database from this file """
    f = open('cars.sql', 'r')
    with f:
        data = f.read()
        return data
        
# Create the database in memory
con = lite.connect(':memory:')

with con:   
    cur = con.cursor()
    sql = readData()
    cur.executescript(sql)
    cur.execute("SELECT * FROM stocks")
    rows = cur.fetchall()
    for row in rows:
        print row
