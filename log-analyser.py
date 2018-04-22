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
            FROM articles JOIN log
            ON log.path = concat('/article/', articles.slug)
            GROUP BY articles.title
            ORDER BY article_views DESC
            LIMIT 3;
    """

    # Execute the above query.
    results = execute_query(query)

    # Print the result.
    print("----------------------------------------------------------------")
    print("\t\tI. TOP THREE ARTICLES OF ALL TIME")
    print("----------------------------------------------------------------")
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
        SELECT authors.name, COUNT(*) AS num
        FROM authors JOIN articles
        ON authors.id = articles.author
        JOIN log
        ON log.path = concat('/article/', articles.slug)
        GROUP BY authors.name
        ORDER BY num DESC
    """

    # Run Query
    results = execute_query(query)

    # Print Results
    print("\n\n----------------------------------------------------------------")
    print("\t\tII. POPULAR AUTHORS OF ALL TIME")
    print("----------------------------------------------------------------")
    rank = 1
    for row in results:
        print(u"  {0}. {1} — {2:,} views.".format(rank, row[0], row[1]))
        rank += 1


def get_days_with_errors():
    """returns days with more than 1% errors"""

    # Build Query String
    query = """
        SELECT total.day,
          ROUND(((errors.error_requests*1.0) / total.requests), 3) AS percent
        FROM (
          SELECT date_trunc('day', time) "day", count(*) AS error_requests
          FROM log
          WHERE status LIKE '404%'
          GROUP BY day
        ) AS errors
        JOIN (
          SELECT date_trunc('day', time) "day", count(*) AS requests
          FROM log
          GROUP BY day
          ) AS total
        ON total.day = errors.day
        WHERE (ROUND(((errors.error_requests*1.0) / total.requests), 3) > 0.01)
        ORDER BY percent DESC;
    """

    # Run Query
    results = execute_query(query)

    # Print Results
    print("\n\n----------------------------------------------------------------")
    print("   III. DAYS IN WHICH MORE THAN 1% OF REQUESTS LEAD TO ERRORS")
    print("----------------------------------------------------------------")
    for row in results:
        date = row[0].strftime('%B %d, %Y')         # Pretty-formatting date.
        errors = str(round(row[1]*100, 1)) + "%" + " errors"
        print("   " + date + u" — " + errors)


if __name__ == '__main__':
    get_popular_articles()
    get_popular_authors()
    get_days_with_errors()
