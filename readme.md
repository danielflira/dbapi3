# dbapi3

Adds some facilities to use pure dbapi2, and a simple database migration system

## Getting Started

Just create an database object instance and send commands to database :)

```python3
# Import the module and used driver
from dbapi3 import Database
import sqlite3

# Create an new database connection
db = Database(sqlite3, 'my.db')

# Just execute some statement
try:
	db.execute('create table person(name varchar(100))').c.commit()
except db.d.ProgrammingError as e:
	print(e)

# db has a reference to driver used to create connection
# execute return a cursor with a reference to connection
```

### Prerequisites

- python2.7
- python3.5
- pypy3.5

### Installing

To install just use repository and pip

```bash
# pip3 install https://github.com/danielflira/dbapi3.git
or
# pip3 install https://github.com/danielflira/dbapi3/archive/master.zip
```

## Running the tests

To run test you must use drone.io you can run locally with

```bash
# drone exec
```

## Authors

* **Daniel Lira** - *Initial work* - [dbapi3h](https://github.com/danielflira/dbapi3)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
