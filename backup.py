#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys


def writeData(data):
    f = open('cars.sql', 'w')
    with f:
        f.write(data)

conn = lite.connect(r"notes_ARGH.db")


with conn:
    cur = conn.cursor()
    
    
    data = '\n'.join(conn.iterdump())
    
    writeData(data)
