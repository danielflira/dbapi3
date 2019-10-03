# database

dbapi-2 helper library

# Using

Consider de following code where some table is created, inserted and selected.

```
from database import Database
import sqlite3
import logging

db = Database(sqlite3, 'database.db')

try:
    db.execute('''CREATE TABLE person (name VARCHAR(100))).c.commit()
except db.d.ProgrammingError as e:
    logging.warn(e)

try:
    db.execute('''INSERT INTO person VALUES(?)''', ('yourname',)).c.commit()
except db.d.ProgrammingError as e:
    loggin.warn(e)

for row in db.execute('''SELECT * FROM person'''):
    print(row)
```

To change my RDBMS once my SQL instructions work on another, just change

```
from database import Database
import pypyodbc

db - Database(pypyodbc, 'Driver={PotsgreSQL ANS}...')
```

Two main attributes on Database instance is d for driver use to connect and c to connection associated with cursor returned by execute*. This way you can access all components from an database instruction on a simple way.
