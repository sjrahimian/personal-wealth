# -*- coding: utf-8 -*-
# database.py

# Built-in libraries
from pathlib import Path
import sqlite3
from sqlite3 import Error
import sys


# Custom libraries
import schemas

""" This will contain all the save/load/query methods for the different databases.

    Upon starting the program, the 'management' database will be loaded first which contains 
    the various user's workspace accounts. From this list the user will select the specific 'workspace' 
    database, which contains the desired wealth data (such as income, expenditures, etc.).
    The user should be able to close the 'workspace' database and open another 'workspace' 
    database. As such, a maximum of two databases may be loaded at any particular time.

"""

# user-defined database exceptions
class DatabaseError(Exception):
"""Base class for database exceptions"""
    pass

class DatabaseTableInsertError(DatabaseError):
    """Raised when the not able to insert into table"""
    pass

class Database():
    """ Interface to SQLite3 database; defines basic methods needed. """

    def __init__(self, path="bin/resources/", fn="database.db"):
        """ Create or connect to the appropriate database provided by user.

        Args:
            path (str, optional): Database path. Defaults to "bin/resources/".
            fn (str, optional): Database filename. Defaults to "database.db".
        """
        self.file = Path(path, fn)
        if not self.file.exists():
            self.db = self.create(dbFile)
        else:
            self.db = self.load()

    def load(self):
        """ Create a database connection specified by file

        Returns:
            sqlite3.Connection: Connection for database object
            None: None (when unable to connect/load database)
        """

        try:
            conn = sqlite3.connect(self.file)
            return conn
        except Error as e:
            print(f"Failed to load database file: \n {e}")
            return None

    def create(self, *schemas):
        """ Create a database specified by file and the table(s) according to the schemas.

        Args:
            schemas (str, set, list, tuple): the schema to create the database tables

        Returns:
            sqlite3.Connection: Connection for database object
            None: None (when unable to connect/load database)
        """

        print("Creating new database...")
        try:
            if (conn:= self.load(self.file)) is not None:

                # Create tables
                cur = conn.cursor()
                for schema in schemas:
                    try:
                        cur.execute(schema)
                        self.save()

                    except Error as e:
                        print(f"TableCreationFailed :: {e}\n{schema}")


                print("...creation complete.")
                return conn
            else:
                raise ManagementDatabaseError(f"Failed to connect and create database {self.file}")

        except DatabaseError as e:
            print(f"{e}")
            
    def insert(self, query=None, data=None):
        """ Insert the data into the desired table. Query example:
                1. 'INSERT INTO tableA (x, y, datatime) VALUES (?,?,?);'
                2. 

        Args:
            query (str, optional): The query to insert into the table. Defaults to None.
            data (str, list, set, tuple, optional): The data to be inserted into the table. Defaults to None.

        Raises:
            DatabaseTableInsertError: when query or data are not provied by user

        Returns:
            int: successful insert or failed to insert
        """

        try:
            msg = "Cannot insert into table without"
            if query is None:
                raise DatabaseTableInsertError(msg, "query.")
            elif data is None:
                raise DatabaseTableInsertError(msg, "data.")


        except DatabaseTableInsertError as e:
            print(e)
            return 1

        # insert into table
        cur = self.db.cursor()
        cur.execute(query, data)
        self.save()

        return 0

    def close(self):
        """ Close the database """
        self.save()
        if self.db:
            self.db.close()

    def save(self):
        self.db.commit()
    
    def cursor(self):
        return self.db.cursor()


class ManagementDB(Database):
    """ Mangaement database interface """

    def __init__(self):
        super().__init__(fn="management.db")

    def create(self):
        super().create(schemas.Management())


class WorkSpaceDB(Database):
    """ Workspace database interface """

    def __init__(self, fn="workspace.db"):
        super().__init__(fn=fn)
    
    def create(self):
        super().create(schemas.WorkSpace())
