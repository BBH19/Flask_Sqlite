import sqlite3
from flask import Flask


app = Flask("Test")
conn = sqlite3.connect("persons.sqlite")

cursor = conn.cursor()
sql_query = """CREATE TABLE person(
    id integer PRIMARY KEY,
    firstName text NOT NULL,
    lastName text NOT NULL
    )"""
    
cursor.execute(sql_query)

