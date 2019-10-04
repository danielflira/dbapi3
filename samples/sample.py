#!/usr/bin/env python3

import sqlite3
import logging

from dbapi3 import Database

db = Database(sqlite3, ':memory:')

try:
    db.execute('CREATE TABLE person (name VARCHAR(100), age INTEGER)').c.commit()
except Exception as e:
    logging.error(e)

try:
    person = ('me', 10)
    db.execute('''INSERT INTO person VALUES(?, ?)''', person).c.commit()
except db.d.ProgrammingError as e:
    logging.error(e)

try:
    people = (('you', 20), ('he', 30),)
    db.executemany('''INSERT INTO person VALUES(?, ?)''', people).c.commit()
except db.d.ProgrammingError as e:
    logging.error(e)

for row in db.execute('SELECT * FROM person'):
    print(row)

for row in db.execute('SELECT * FROM person').as_dict():
    print(row)

db.c.close()