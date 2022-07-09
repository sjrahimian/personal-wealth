# -*- coding: utf-8 -*-
# schemas.py

import sys
import sqlite3

    """Contains the table schemas to build the databases when there are none.
        
        Two types of files can be built with these schemas:
            - 'accounts' database contains the various user's wealth accounts. 
            - 'wealth' database contains the wealth data (such as income, expenditures, etc.).

    """

class AccountTable():
    tbl_account = """ 
        CREATE TABLE "Account" (
            "uuid"	INTEGER NOT NULL UNIQUE,
            "account_name"	INTEGER NOT NULL UNIQUE,
            "first_name"	INTEGER NOT NULL,
            "last_name"	TEXT NOT NULL,
            PRIMARY KEY("uuid")
        ) WITHOUT ROWID
    """

    def __init__(self):
        pass


class WealthTables():
    tbl_setting = """
        CREATE TABLE "Setting" (
            "uuid"	TEXT NOT NULL UNIQUE,
            "country"	TEXT NOT NULL DEFAULT 'Canada',
            "currency"	TEXT NOT NULL DEFAULT 'CAD',
            "fiscal_start"	TEXT NOT NULL DEFAULT '01-01',
            PRIMARY KEY("uuid")
        ) WITHOUT ROWID
    """

    tbl_income = """
        CREATE TABLE "Income" (
            "uiid"	INTEGER NOT NULL UNIQUE,
            "amount"	NUMERIC NOT NULL,
            "type"	TEXT NOT NULL,
            "description"	BLOB,
            "tags"	BLOB NOT NULL,
            "category"	BLOB NOT NULL,
            "datetime"	INTEGER NOT NULL,
            PRIMARY KEY("uiid" AUTOINCREMENT)
        )
    """

    def __init__(self):
        pass