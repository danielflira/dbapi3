#!/usr/bin/env python3


class Wrap:
    '''
    Redirect object attr access to original
    '''

    def __init__(self, other):
        self.other = other

    def __getattr__(self, attr):
        return getattr(self.other, attr)


class Cursor(Wrap):
    '''
    Offers generic cursor functionalities or proxy to native
    '''

    def __init__(self, other):
        Wrap.__init__(self, other)

    def __iter__(self):
        return self.other.__iter__()

    def as_dict(self):
        '''
        Return row with column names
        '''

        headers = [i[0] for i in self.description]
        for row in self:
            yield dict(zip(headers, row))


class Connection(Wrap):
    '''
    Offers generic connection functionalities or proxy to native
    '''

    def __init__(self, other):
        Wrap.__init__(self, other)


class Database:
    '''
    Connects to a database through given driver.

    Receives driver and driver's attributes, create new connections
    through driver and expose driver as d attribute
    '''

    def __init__(self, driver, *args, **kwargs):
        self.d = Wrap(driver)
        self.args = args
        self.kwargs = kwargs
        self._connect()

    def _connect(self):
        self.c = Connection(self.d.connect(*self.args, **self.kwargs))

    def _normalize(self, statement, args=None, kwargs=None):
        if args == None:
            args = []

        if kwargs == None:
            kwargs = {}

        if self.d.paramstyle == 'qmark':
            return statement, args

        elif self.d.paramstyle == 'numeric':
            nstatement = ''
            place = 1

            for i, c in enumerate(statement):
                if c == '?' and statement[i-1] != '\\':
                    nstatement += ':' + str(place)
                    place += 1
                else:
                    nstatement += c

            return nstatement, args

        elif self.d.paramstyle == 'named':
            nstatement = ''
            nparams = {}
            name = 'a'
            place = 1

            for i, c in enumerate(statement):
                if c == '?' and statement[i-1] != '\\':
                    nstatement += ':' + name
                    nparams[name] = args[place]
                    name += 'a'
                    place += 1
                else:
                    nstatement += c

            return nstatement, nparams

        elif self.d.paramstyle == 'format':
            nstatement = ''
            place = 0

            for i, c in enumerate(statement):
                if c == '?' and statement[i-1] != '\\':
                    t = type(params[place])

                    if t == float:
                        nstatement += '%f'
                    elif t == int:
                        nstatement += '%d'
                    else:
                        nstatement += '%s'

                    place += 1
                else:
                    nstatement += c

            return nstatement, args

        elif self.d.paramstyle == 'pyformat':
            nstatement = ''
            nparams = {}
            name = 'a'
            place = 0

            for i, c in enumerate(statement):
                if c == '?' and statement[i-1] != '\\':
                    t = type(args[place])

                    # if t == float:
                    #     nstatement += '%(' + name + ')f'
                    # elif t == int:
                    #     nstatement += '%(' + name + ')d'
                    # else:
                    #     nstatement += '%(' + name + ')s'

                    nstatement += '%(' + name + ')s'

                    nparams[name] = args[place]
                    name += 'a'
                    place += 1
                else:
                    nstatement += c

            return nstatement, nparams

    def execute(self, statement, *args, **kwargs):
        '''
        Same interface as dbapi-2 execute, receive an statement and parameters,
        as return gives a "soft" cursor.

        For more info: https://www.python.org/dev/peps/pep-0249/#id15
        '''

        statement, params = self._normalize(statement, *args, **kwargs)

        cursor = Cursor(self.c.cursor())
        cursor.execute(statement, params)
        cursor.c = self.c
        return cursor

    def executemany(self, statement, *args, **kwargs):
        '''
        Same interface as dbapi-2 executemany, receive an statement and a lista of parameters,
        as return gives a "soft" cursor.

        For mor info: https://www.python.org/dev/peps/pep-0249/#executemany
        '''

        cursor = Cursor(self.c.cursor())
        cursor.executemany(statement, *args, **kwargs)
        cursor.c = self.c
        return cursor

    def migrate(self, migrations):
        try:
            self.execute('''
                CREATE TABLE dbapi3_migration(
                    namespace VARCHAR(25) not null,
                    version INTEGER not null,
                    description VARCHAR(100) not null)
            ''').c.commit()
        except:
            self.c.rollback()

        for m in migrations:

            r = self.execute('''
                SELECT MAX(version) as max
                FROM dbapi3_migration
                WHERE 1=1
                    AND namespace = ?
            ''', (m.namespace,))

            for row in r.as_dict():
                version = row['max']

            if version != None and m.version <= version:
                continue

            if m.function(self, m.description) != True:
                self.c.rollback()
                raise MigrationException("\"{}\" failed!".format(m.description))

            self.execute('''
                INSERT INTO dbapi3_migration VALUES (?, ?, ?)
            ''', (
                m.namespace,
                m.version, 
                m.description,
            )).c.commit()


class Migration:
    def __init__(self, namespace, version, function, description):
        self.namespace = namespace
        self.version = version
        self.function = function
        self.description = description


class MigrationException(Exception):
    pass