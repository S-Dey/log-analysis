#!/usr/bin/env python3
import psycopg2

DBNAME = "news"


def execute_query(query):
    """Connect to the database and execute the query passed to it.

    Argument:
        query (string) -- The SQL query to execute.

    Returns:
        rows (list) -- A list of the resultant rows.
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


# --------------------------------------------------------------
# 1. TOP THREE ARTICLES OF ALL TIME
# --------------------------------------------------------------
def get_popular_articles():
    """Return top three popular articles of all time."""

    query = """
        SELECT articles.title, COUNT(*) AS article_views
            FROM articles INNER JOIN log
            ON log.path LIKE concat('/article/%', articles.slug)
            GROUP BY articles.title
            ORDER BY article_views DESC
            LIMIT 3;
    """

    # Execute the above query.
    results = execute_query(query)

    # Print the result.
    print('\nTOP THREE ARTICLES BY PAGE VIEWS:')
    count = 1
    for row in results:
        number = '(' + str(count) + ') "'
        title = row[0]
        views = '" with ' + str(row[1]) + " views"
        print(number + title + views)
        count += 1


if __name__ == '__main__':
    get_popular_articles()
