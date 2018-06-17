#!/usr/bin/env python3
import sys
import psycopg2

"""Module to analyse the log and print desired results.

It prints the results of the following problems from the 'news'
database:
    1. What are the most popular three articles of all time?
    2. Who are the most popular article authors of all time?
    3. On which days did more than 1% of requests lead to errors?

All the queries are written for PostgreSQL DBMS. More details can
be found in the README.md file, which is included with this project.
"""

__author__ = 'Subhadeep Dey'


def execute_query(query):
    """Establish connection with database and execute the query passed to it.

    Argument:
        query (string) -- The SQL query to execute.

    Returns:
        rows (list) -- A list of resultant rows.

    """
    try:
        conn = psycopg2.connect('dbname=news')
        c = conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        conn.close()
        return rows
    except psycopg2.Error as e:
        print(e)
        sys.exit(1)


# --------------------------------------------------------------
# 1. TOP THREE ARTICLES OF ALL TIME
# --------------------------------------------------------------
def get_popular_articles():
    """Return top three popular articles of all time."""
    query = """
        SELECT articles.title, COUNT(*) AS article_views
            FROM articles JOIN log
            ON log.path = concat('/article/', articles.slug)
            GROUP BY articles.title
            ORDER BY article_views DESC
            LIMIT 3;
    """

    # Execute the above query.
    results = execute_query(query)

    # Print results.
    print("--------------------------------------------------------------")
    print("\t\tI. TOP THREE ARTICLES OF ALL TIME")
    print("--------------------------------------------------------------")
    rank = 1
    for row in results:
        print(u"  {0}. \"{1}\" — {2:,} views.".format(rank, row[0], row[1]))
        rank += 1


# --------------------------------------------------------------
# 2. POPULAR AUTHORS OF ALL TIME
# --------------------------------------------------------------
def get_popular_authors():
    """Return authors sorted by page views."""
    query = """
        SELECT authors.name, COUNT(*) AS views
            FROM authors JOIN articles
                ON authors.id = articles.author
            JOIN log
                ON log.path = concat('/article/', articles.slug)
            GROUP BY authors.name
            ORDER BY views DESC
    """

    # Run above query.
    results = execute_query(query)

    # Print results.
    print("\n\n--------------------------------------------------------------")
    print("\t\tII. POPULAR AUTHORS OF ALL TIME")
    print("--------------------------------------------------------------")
    rank = 1
    for row in results:
        print(u"  {0}. {1} — {2:,} views.".format(rank, row[0], row[1]))
        rank += 1


# --------------------------------------------------------------
# 3. DAYS IN WHICH MORE THAN 1% OF REQUESTS LEAD TO ERRORS
# --------------------------------------------------------------
def get_days_with_errors():
    """Return days in which more than 1% requests lead to errors."""
    query = """
        SELECT total.day,
          ROUND(((errors.err_requests * 100.0) / total.requests), 5) AS percent
        FROM (
              SELECT date_trunc('day', time) AS day, count(*) AS err_requests
              FROM log
              WHERE status LIKE '404%'
              GROUP BY day
            ) AS errors
        JOIN (
              SELECT date_trunc('day', time) AS day, count(*) AS requests
              FROM log
              GROUP BY day
            ) AS total
        ON total.day = errors.day
        WHERE (ROUND(((errors.err_requests * 100.0)/total.requests), 5) > 1.0)
        ORDER BY percent DESC;
    """

    # Execute the above query.
    results = execute_query(query)

    # Print results.
    print("\n\n--------------------------------------------------------------")
    print("  III. DAYS IN WHICH MORE THAN 1% OF REQUESTS LEAD TO ERRORS")
    print("--------------------------------------------------------------")
    for row in results:
        date = row[0].strftime('%B %d, %Y')     # Pretty-formatting date.
        errors = str(round(row[1], 2)) + "%" + " errors"
        print("   " + date + u" — " + errors)


# Print all the results.
if __name__ == '__main__':
    get_popular_articles()
    get_popular_authors()
    get_days_with_errors()
