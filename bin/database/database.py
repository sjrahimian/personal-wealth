# -*- coding: utf-8 -*-
# database.py

from pathlib import Path
import sqlite3
from sqlite3 import Error
import sys

""" This will contain all the save/load/query methods for the different databases.

    Upon starting the program, the 'account' database will be loaded first which contains 
    the various user's wealth accounts. From this list the user will select the specific 'wealth' 
    database, which contains the desired wealth data (such as income, expenditures, etc.).
    The user should be able to close the 'wealth' database and open another 'wealth' 
    database. As such, a maximum of two databases will be loaded at a particular time.

"""

class Database()
    def __init__(self):
        pass

    def save(self):
        pass  

    def load(self):
        pass

class AccountDB()
    def __init__():
        pass

class WealthDB()
    def __init__():
        pass
