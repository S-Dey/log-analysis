#!/usr/bin/env python3
import psycopg2

DBNAME = "news"


def execute_query(query):
    """Connect to the database and execute the query passed to it.

    Argument:
        query (string) -- The SQL query to execute.

    Returns:
        rows (list) -- A list of the resultant row(s).
    """

    try:
        conn = psycopg2.connect("dbname=" + DBNAME)
        c = conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        conn.close()
        return rows
    except psycopg2.Error as e:
        print(e)
