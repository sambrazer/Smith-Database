import sqlite3
import datetime
import math
import re

conn = sqlite3.connect('smithsdb.sqlite')
cur = conn.cursor()

#Clear out old data each time a new collection is started.
# This should be run at least once a day; after first run, do not run again until agg is ran (to save entry data)
def daily_entries():
    cur.executescript('''

    DROP TABLE IF EXISTS Entries;

    CREATE TABLE Entries (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        members_id INTEGER,
        username TEXT,
        start TEXT,
        date DATE,
        activity TEXT
    )
    ''')

def initial_tables():
    # Clears tables then creates tables for database. This should only be run once. Running multiple times will clear data

    cur.executescript('''
    DROP TABLE IF EXISTS Members;
    DROP TABLE IF EXISTS Activities;
    DROP TABLE IF EXISTS Aggregate;

    CREATE TABLE Members (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        b_day DATE,
        email TEXT,
        phone TEXT NOT NULL,
        username TEXT
    );

    CREATE TABLE Activities (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        activity_name TEXT NOT NULL UNIQUE,
        status INTEGER NOT NULL
    );

    CREATE TABLE Aggregate (
        entries_id INTEGER,
        members_id INTEGER,
        username TEXT,
        start TEXT,
        leave TEXT,
        date DATE,
        activity TEXT,
        PRIMARY KEY (members_id, entries_id)
    )
''')
