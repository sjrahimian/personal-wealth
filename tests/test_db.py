
from datetime import datetime
import json

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
            "col_B"	TEXT NOT NULL,
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

def test_database_extract_all_empty_table():
    query = "SELECT * FROM table02;"
    results = db.fetchall(query)

    assert results == None

def test_database_extract_all():
    helper_insertMany()
    query = "SELECT * FROM table01;"
    results = db.fetchall(query)

    assert results == [('foo',  datetime.now().strftime("%m-%d"))]

def test_database_extract_all_fail_syntaxError():
    # helper_insertMany()
    query = "SELECT FROM table01;"
    results = db.fetchall(query)
    print(results)

    assert results == -1

def test_database_delete():
    print(db.file)
    assert db.delete() == False

def test_ManagementDB():
    db = database.ManagementDB()
    db.create
    assert db.delete() == False

def test_WorkspaceDB():
    db = database.WorkspaceDB()
    db.create
    assert db.delete() == False

### Helper functions
def helper_insertMany():
    jsonSample = {"yaml": "markup", "Lorem": ['ipsum', 'dolor'], "foo": {"bar":"barbar", "foo": "foofoo"}}

    query = 'INSERT INTO table02 (col_A, col_B, col_C) VALUES (?,?,?);'
    data = [("foo", "cat\n1231", datetime.now()),
            ("bar", 9876, datetime.now()),
            ("foofoo", json.dumps(jsonSample), datetime.now()),
            ("foobar", "\t\tchedder\n\n\t\tcheese\n\n", datetime.now())]

    for d in data:
        x = db.insert(query, d)
        print(x)

    print("fin")