#!/usr/bin/env python3
import psycopg2

DBNAME = "news"


def execute_query(query):
    """Connect to the database and execute the query passed to it.

    Argument:
    query (string) -- The query to execute.
    """

    # Connect to the database.
    try:
        conn = psycopg2.connect("dbname=" + DBNAME)
    except psycopg2.Error as e:
        print("{} : {}".format(e.pgerror, e.pgerror))

    # Execute query and fetch rows.
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows

