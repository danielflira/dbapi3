#!/usr/bin/env python3

import sqlite3
import logging

from dbapi3 import Database

db = Database(sqlite3, ':memory:')

try:
    db.execute('create table test (test varchar(100))').c.commit()
except Exception as e:
    logging.error(e)

try:
    db.execute('''insert into test values('test')''').c.commit()
except db.d.ProgrammingError as e:
    loggin.error(e)

for row in db.execute('select * from test'):
    print(row)

for row in db.execute('select * from test').as_dict():
    print(row)

db.c.close()