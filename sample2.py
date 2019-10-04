#!/usr/bin/env python3

import sqlite3
import logging

from dbapi3 import Database, Migration

db = Database(sqlite3, 'sample2.db')


def migration_v1(dbx, description):
    logging.error(description)

    try:
        dbx.execute(
            'CREATE TABLE person (name VARCHAR(100), age INTEGER)').c.commit()
    except Exception as e:
        logging.error(e)


def migration_v2(dbx, description):
    logging.error(description)

    try:
        person = ('me', 10)
        dbx.execute('''INSERT INTO person VALUES(?, ?)''', person).c.commit()
    except db.d.ProgrammingError as e:
        logging.error(e)

    try:
        people = (('you', 20), ('he', 30),)
        dbx.executemany('''INSERT INTO person VALUES(?, ?)''',
                        people).c.commit()
    except db.d.ProgrammingError as e:
        logging.error(e)


migrations = [
    Migration(1, migration_v1, "Criacao das tabelas"),
    Migration(2, migration_v2, "Insercao dos dados"),
]

db.migrate(migrations)

for row in db.execute('SELECT * FROM person'):
    print(row)

for row in db.execute('SELECT * FROM person').as_dict():
    print(row)

db.c.close()
