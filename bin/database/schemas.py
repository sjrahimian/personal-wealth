# -*- coding: utf-8 -*-
# schemas.py

import sys
import sqlite3

"""Contains the table schemas to build the databases when there are none.
    
    Two types of files can be built with these schemas:
        - 'management' database contains the various user's workspaces. 
        - 'workspace' database contains the wealth data (such as income, expenditures, etc.).

"""

class Management():
    management = """ 
        CREATE TABLE "management" (
            "workspace_id"	TEXT NOT NULL UNIQUE,
            "first_name"	TEXT NOT NULL,
            "last_name"	TEXT NOT NULL,
            PRIMARY KEY("workspace_id")
        ) WITHOUT ROWID
    """

    all_tables = { management }

    def __init__(self):
        return all_tables


class WorkSpace():
    setting = """
        CREATE TABLE "setting" (
            "workspace_id"	TEXT NOT NULL UNIQUE,
            "country"	TEXT NOT NULL DEFAULT 'Canada',
            "currency"	TEXT NOT NULL DEFAULT 'CAD',
            "fiscal_start"	INTEGER NOT NULL DEFAULT '01-01',
            PRIMARY KEY("workspace_id")
        ) WITHOUT ROWID
    """

    income = """
        CREATE TABLE "Income" (
            "uiid"	TEXT NOT NULL UNIQUE,
            "amount"	REAL NOT NULL,
            "type"	TEXT NOT NULL CHECK(type == "active" OR type == "passive" OR type == "portfolio"),
            "description"	TEXT NOT NULL,
            "tags"	BLOB NOT NULL,
            "category"	BLOB NOT NULL,
            "datetime"	INTEGER NOT NULL,
            PRIMARY KEY("uiid")
        )
    """

    all_tables = { setting, income }

    def __init__(self):
        return all_tables