#!/usr/bin/python
'''
File: merge-emojis.py
Author: Oliver Uvman
Description:
    Usage: ./merge-emojis.py <OUTPUT> <INPUT> <INPUT> [...]

    Reads any number of input files, each is assumed to be
    of emoji-db form. Saves all emoji key-values encountered.

    When encountering duplicate keys, overwrites previous value
    with the value from the latter db-file. Finally appends all
    emojis to output file, sorted by value so any duplicate
    values appear next to each other.

    Any values that would be overwritten due to key conflicts
    are appended at the end of the file, with their previous
    key slightly mutated to become unique.

    Reports on stdout if there are duplicate values or if
    any values had their keys changed.

    Guarantees that no value is lost, though some might get
    new namess
License: Pubic domain :)
'''

import sys

if (len(sys.argv) < 4):
    print r'./merge-emojis.py <OUTPUT> <INPUT> <INPUT> [...]'
    sys.exit()

output = open(sys.argv[1], 'a')
emojis = {}
overwrittenEmojis = []

for inputFileKey in sys.argv[2:]:
    inputFile = open(inputFileKey, 'r')
    keyLine = True
    emojiKey = ""

    for line in inputFile:
        thisLine = line.rstrip('\n')
        if keyLine == True:
            keyLine = False
            emojiKey = thisLine
        else:
            keyLine = True
            if (emojiKey in emojis) and emojis[emojiKey] != thisLine:
                overwrittenEmojis.append((emojiKey, emojis[emojiKey]))
            emojis[emojiKey] = thisLine

# emojis is now a list of unique keys with values.
# A value can exist several times, with different keys.

updatedEmojis = []  # Emojis values that might have lost old keys
deletedEmojis = []
for (key, value) in overwrittenEmojis:
    if value in emojis.values():
        updatedEmojis.append(value)
    else:
        deletedEmojis.append((key, value))

busyKeys = emojis.keys()

renamedEmojis = []
renameLog = []
for (key, value) in deletedEmojis:
    newKey = key[:-1] + 'X' + key[-1:]
    while(newKey in busyKeys):
        newKey = newKey[:-1] + 'X' + newKey[-1:]
    renamedEmojis.append((newKey, value))
    renameLog.append((value, key, newKey))
    busyKeys.append(newKey)

emojisByValue = sorted(emojis.items(), key=lambda emo: (emo[1], emo[0]))

for (key, value) in emojisByValue:
    output.write(key + '\n')
    output.write(value + '\n')

for (key, value) in renamedEmojis:
    output.write(key + '\n')
    output.write(value + '\n')

if updatedEmojis:
    print 'The following emojis have had their keys updated:'
    for value in updatedEmojis:
        print value, ' is now known as:'
        for (key, ivalue) in emojisByValue + renamedEmojis:
            if value == ivalue:
                print '\t', key

if renamedEmojis:
    print 'The following emojis have lost their keys\nbut have new keys at the end of the file:'
for (value, oldKey, newKey) in renameLog:
    print value, 'renamed from', oldKey, 'to', newKey
