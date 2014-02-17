#!/usr/bin/env python

""" Provides a notes object that can be queried and updated """

import sqlite3
import datetime
import base62

class Notes():
    def __init__(self):
        pass
   
    def createDatabase(self):
        """ The goal here is to ensure we have a sane/working default DB """
        conn = self.__openAndGetConnection()
        cur = conn.cursor()
        # Drop it if it already exists
        cur.execute("DROP TABLE IF EXISTS notes")
        # Make a new shiny one
        cur.execute('''CREATE TABLE IF NOT EXISTS notes
             (id INTEGER PRIMARY KEY, hits INT, title TEXT, author TEXT, note TEXT, creation TIMESTAMP, expiration TIMESTAMP)''')
        tempStamp = datetime.datetime.now()

        self.addNote("This is the first note in the database", expiration=tempStamp);
        
        # Commit it all
        conn.commit()
        self.__close(conn)
        
    def addNote(self, note, title="Untitled Wonder", expiration=None, author=u"Anonymous"):
        if not expiration:
            # Limit to 1 hour
            expiration = datetime.datetime.now() + (datetime.timedelta(hours=1))
            
        # Make with the unicode
        note = unicode(note)
        title = unicode(title)
        author = unicode(author)
        
        # Open it up and slap it in
        conn = self.__openAndGetConnection()
        cur = conn.cursor()
        
        demoNote = (0, title, author, note, datetime.datetime.now(), expiration) 
        cur.execute('''INSERT INTO notes VALUES (NULL, ?, ?, ?, ?, ?, ?)''', demoNote)
        retVal = cur.lastrowid
        conn.commit()
        self.__close(conn)
        return base62.fromInt(retVal)
        
    def __openAndGetConnection(self):
        """ Open the database and hand back tuples """
        return sqlite3.connect(r"notes_ARGH.db")
        
    def __close(self, connection):
        connection.close()
    
    def getAllNotes(self):
        """ Should be able to get all notes and key value that shit - doesn't update the hit count """
        conn = self.__openAndGetConnection()
        cur = conn.cursor()
        cur.execute('''SELECT * FROM notes''')
        conn.commit()
        retVal = cur.fetchall()
        self.__close(conn)
        return retVal
        
    def getAllNoteIDs(self):
        conn = self.__openAndGetConnection()
        cur = conn.cursor()
        cur.execute('''SELECT id,title FROM notes''')
        conn.commit()
        retVal = cur.fetchall()
        if retVal:
            retVal = [(base62.fromInt(i[0]),i[1]) for i in retVal]
        self.__close(conn)
        return retVal
    
    def getNoteByID(self, noteID):
        """ 
            Gets a note with from a given hashed ID - updates the hit count
        """
        val = (base62.toInt(unicode(noteID)),)
        conn = self.__openAndGetConnection()
        cur = conn.cursor()
        cur.execute('''UPDATE notes SET hits = hits + 1 WHERE id=(?)''', val)
        cur.execute('''SELECT hits, title, author, note, creation, expiration FROM notes WHERE id=(?)''', val)
        conn.commit()
        retVal = cur.fetchone()
        self.__close(conn)
        return retVal
        
    def deleteNoteByID(self, noteID):
        """ Should allow the deleting of a specific note by the hashed ID """
        val = (base62.toInt(unicode(noteID)),)
        conn = self.__openAndGetConnection()
        cur = conn.cursor()
        cur.execute('''DELETE FROM notes WHERE id=(?)''', val)
        conn.commit()
        self.__close(conn)        
        
    def deleteNoteByKey(self, noteKey):
        """ Should allow the deleting of a specific note by primary key directly """
        conn = self.__openAndGetConnection()
        cur = conn.cursor()
        cur.execute('''DELETE FROM notes WHERE id=(?)''', (noteKey,))
        conn.commit()
        self.__close(conn)
        
        
    def purgeOldKeys(self):
        """ Delete any posts older than today """
        conn = self.__openAndGetConnection()
        cur = conn.cursor()
        cur.execute('''DELETE FROM notes WHERE expiration < (?)''', (datetime.datetime.now(),))
        conn.commit()
        self.__close(conn)
