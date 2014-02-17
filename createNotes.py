#!/usr/bin/env python

""" Test harness for notes """

from notes import Notes
import base62

foo = Notes()

foo.createDatabase()
print "Inserting with ID", foo.addNote("This is a test", title="First Post")
print "Inserting with ID", foo.addNote("XXX This is a another test XXX", author="Nick")

for row in foo.getAllNotes():
    print row
    print base62.fromInt(row[0])

print foo.getAllNoteIDs()

print "Check Hits"    
print foo.getNoteByID(u"aaaaaaaaaab")
print foo.getNoteByID(u"aaaaaaaaaab")
foo.deleteNoteByID("aaaaaaaaaab")
foo.deleteNoteByKey(2)
print foo.getNoteByID(u"aaaaaaaaaab")


print "\nPurging notes"
foo.purgeOldKeys()

print "\nListing notes"
for row in foo.getAllNotes():
    print row
    print base62.fromInt(row[0])
