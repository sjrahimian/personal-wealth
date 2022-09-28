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
            "workspace_title"   TEXT NOT NULL,
            "first_name"	TEXT NOT NULL,
            "last_name"	TEXT NOT NULL,
            "datetime"	INTEGER NOT NULL,
            PRIMARY KEY("workspace_id")
        ) WITHOUT ROWID
    """

    all_tables = { management }

    def __init__(self):
        return all_tables


class WorkSpace():
    income = """
        CREATE TABLE "Income" (
            "uiid"	TEXT NOT NULL UNIQUE,
            "amount"	REAL NOT NULL,
            "type"	TEXT NOT NULL CHECK(type == "active" OR type == "passive" OR type == "portfolio"),
            "description"	TEXT NOT NULL,
            "tags"	TEXT NOT NULL,
            "category"	TEXT NOT NULL,
            "datetime"	INTEGER NOT NULL,
            PRIMARY KEY("uiid")
        )
    """

    expenditure = """
        CREATE TABLE "expenditure" (
            "ueid"	TEXT NOT NULL UNIQUE,
            "amount"	REAL NOT NULL,
            "type"	TEXT NOT NULL CHECK("type" == "want" OR "type" == "need"),
            "description"	TEXT NOT NULL,
            "category"	TEXT NOT NULL,
            "tags"	TEXT NOT NULL,
            "upid"	TEXT,
            "urid"	TEXT,
            "datetime"	INTEGER NOT NULL,
            PRIMARY KEY("ueid"),
            FOREIGN KEY("urid") REFERENCES "returns"("urid"),
            FOREIGN KEY("upid") REFERENCES "expenditure"("upid")
        )
    """

    mortgage = """
        CREATE TABLE "mortgage" (
            "upid"	TEXT NOT NULL UNIQUE,
            "principle"	REAL NOT NULL,
            "deposit"	REAL NOT NULL,
            "remaing"	REAL NOT NULL,
            "apprasial_value"	REAL,
            "apprasial_date"	INTEGER,
            "datetime"	INTEGER NOT NULL,
            FOREIGN KEY("upid") REFERENCES "properties"("upid"),
            PRIMARY KEY("upid")
        ) WITHOUT ROWID
    """

    properties = """
        CREATE TABLE "properties" (
            "upid"	TEXT NOT NULL UNIQUE,
            "address"	TEXT NOT NULL,
            "mortgages"	TEXT NOT NULL,
            "rental"	TEXT NOT NULL DEFAULT 'False',
            "status"	TEXT NOT NULL CHECK("status" == "primary" OR "status" == "secondary"),
            "category"	TEXT NOT NULL,
            "datetime"	INTEGER NOT NULL,
            PRIMARY KEY("upid")
        ) WITHOUT ROWID
    """
    
    returns = """
        CREATE TABLE "returns" (
            "urid"	TEXT NOT NULL UNIQUE,
            "ueid"	TEXT NOT NULL,
            "amount"	REAL NOT NULL,
            "description"	TEXT NOT NULL,
            "category"	TEXT,
            "tags"	INTEGER,
            "datetime"	INTEGER NOT NULL,
            FOREIGN KEY("ueid") REFERENCES "expenditure"("ueid"),
            PRIMARY KEY("urid")
        ) WITHOUT ROWID
    """

    setting = """
        CREATE TABLE "setting" (
            "workspace_id"	TEXT NOT NULL UNIQUE,
            "country"	TEXT NOT NULL DEFAULT 'canada',
            "currency"	TEXT NOT NULL DEFAULT 'CAD',
            "fiscal_start"	INTEGER NOT NULL DEFAULT '01-01',
            PRIMARY KEY("workspace_id")
        ) WITHOUT ROWID
    """

    all_tables = { income, expenditure, returns, properties, mortgage, setting }

    def __init__(self):
        return all_tables