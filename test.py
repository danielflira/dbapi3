import sqlite3
import pytest
from dbapi3 import Database

def test_connection():
    db = Database(sqlite3, ':memory:')
    db.c.close()

def test_create_table():
    db = Database(sqlite3, ':memory:')
    db.execute('create table teste(teste varchar(10))').c.commit()
    db.c.close()

def test_create_table_fail():
    db = Database(sqlite3, ':memory:')
    with pytest.raises(db.d.OperationalError):
        db.execute('create table with error').c.commit()
