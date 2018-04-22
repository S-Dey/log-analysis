#!/usr/bin/env python3
import psycopg2

DBNAME = "news"


def execute_query(query):
    """Connect to the database and execute the query passed to it.

    Argument:
    query (string) -- The query to execute.
    """
    try:
        conn = psycopg2.connect("dbname=" + DBNAME)
    except psycopg2.Error as e:
        print("Unable to connect to the database.")
