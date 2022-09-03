
from datetime import datetime


from bin.database import database

# New global database for testing
db = database._Database(path="./", fn="db-test.db")

# test functions begin
def test_database():

    t1 = """
        CREATE TABLE IF NOT EXISTS "table01" (
            "col_1"	TEXT NOT NULL UNIQUE,
            "col_2"	INTEGER NOT NULL DEFAULT '01-01',
            PRIMARY KEY("col_1")
        ) WITHOUT ROWID
    """

    t2 = """
        CREATE TABLE IF NOT EXISTS "table02" (
            "col_A"	TEXT NOT NULL UNIQUE,
            "col_B"	BLOB NOT NULL,
            "col_C"	INTEGER NOT NULL,
            PRIMARY KEY("col_A")
        )
    """

    sample_schema = { t1, t2 }
    
    assert db.create(*sample_schema) == 0

def test_database_insert_pass():
    query = 'INSERT INTO table01 (col_1, col_2) VALUES (?,?);'
    data = ("foo", datetime.now().strftime("%m-%d"))

    assert db.insert(query, data) == 0


def test_database_insert_fail_incorrectQ():
    query = 'INSERT INTO table01 (col_1, col2) VALUES (?,?);'
    data = {"foo", '01-01'}

    assert db.insert(query, data) == -1

def test_database_insert_fail_incorrectD():
    query = 'INSERT INTO table01 (col_1, col_2) VALUES (?,?);'
    data = {"foo", 0}

    assert db.insert(query, data) == -1

def test_database_insert_fail_missing():
    query = 'INSERT INTO table01 (col_1, col_2) VALUES (?,?);'

    assert db.insert(query) == -1

def test_database_delete():
    print(db.file)
    assert db.delete() == False
    
