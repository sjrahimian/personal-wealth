# -*- coding: utf-8 -*-
# database.py

# Built-in libraries
from pathlib import Path
import sqlite3
import sys


# Custom libraries
from bin.database import schemas

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

class DatabaseFetchEmpty(DatabaseError):
    """Raised when the not able to extract from table"""
    pass

# Parent database class
class _Database():
    """ Interface to SQLite3 database; defines basic methods needed. """

    def __init__(self, path="bin/resources/", fn="database.db"):
        """ Create or connect to the appropriate database provided by user.

        Args:
            path (str, optional): Database path. Defaults to "bin/resources/".
            fn (str, optional): Database filename. Defaults to "database.db".
        """
        self.db = None
        self.file = Path(path, fn)
        if self.file.exists():
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
        except sqlite3.Error as e:
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

        try:
            if (conn:= self.load()) is not None:

                # Create tables
                cur = conn.cursor()
                
                for schema in schemas:
                    try:
                        cur.execute(schema)

                    except ValueError as e:
                        print("create() function takes an arbitrary number of arguments; unpack data collections before passing in.")
                        return -1
                    except sqlite3.Error as e:
                        print(f"TableCreationFailed :: {e}.\nSchema: {schema}\n")
                        return -1                        

                print("...creation complete.")
                self.db = conn
                self.save()
                
                return 0
                
            else:
                raise DatabaseError(f"Failed to connect and create database {self.file}")

        except DatabaseError as e:
            print(f"{e}")
            self.close()
            return -1
            
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
            if query is None or data is None:
                raise DatabaseTableInsertError(msg, ("query." if query is None else "data."))

            # insert into table
            cur = self.db.cursor()
            cur.execute(query, data)
            self.save()

        except ValueError as e:
            print(e)
            return -1
        except DatabaseTableInsertError as e:
            print(e)
            return -1
        except sqlite3.Error as e:
            print(e)
            return -1
        else:
            return 0
    
    def fetchall(self, query):
        """ Retrieve the data from the desired database using the provided query

        Args:
            query (str, required): The query to fetch the data.

        Raises:
            DatabaseFetchEmpty: no data results are returned or table is empty
            sqlite3.OperationalError: catches any error with SQLite such as query syntax errors

        Returns:
            int: failed to execute query
            None: when no data was retrieved
            results: data fetched from database
        """

        try:
            cur = self.db.cursor()
            cur.execute(query)
            if not (results:= cur.fetchall()):
                raise DatabaseFetchEmpty("\nNo data retrieved.\n")

            return results
        
        except DatabaseFetchEmpty as e:
            print(e)
            return None
        except sqlite3.OperationalError as e:
            print(e)
            return -1
        

    def close(self):
        """ Close the database """
        self.save()
        if self.db:
            self.db.close()

    def save(self):
        self.db.commit()
    
    def cursor(self):
        return self.db.cursor()
        
    def delete(self):
        try:
            self.close()
            self.file.unlink()
        except FileNotFoundError():
            print("Can't delete what can't be found.")
        finally:
            return self.file.exists()


# Children database classes
class ManagementDB(_Database):
    """ Mangaement database interface """

    def __init__(self):
        super().__init__(fn="management.db")

    def create(self):
        super().create(*schemas.Management())


class WorkspaceDB(_Database):
    """ Workspace database interface """

    def __init__(self, fn="workspace.db"):
        super().__init__(fn=fn)
    
    def create(self):
        super().create(*schemas.WorkSpace())
