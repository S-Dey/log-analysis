#!/usr/bin/env python3
import psycopg2


class LogAnalyser:
    """Class to analyse the log and print desired results.

        It prints the results of the following problems from the 'news'
        database:
            1. What are the most popular three articles of all time?
            2. Who are the most popular article authors of all time?
            3. On which days did more than 1% of requests lead to errors?

        All the queries are written for PostgreSQL DBMS. More details can
        be found in the README file, which is included with this project.
    """

    def __init__(self):
        """Establish connection with the database."""
        try:
            self.conn = psycopg2.connect('dbname=news')
            self.c = self.conn.cursor()
        except psycopg2.Error as e:
            print(e)

    def execute_query(self, query):
        """Execute the SQL query passed to it.

        Argument:
            query (string) -- The SQL query to execute.

        Returns:
            rows (list) -- A list of resultant rows.
        """
        self.c.execute(query)
        rows = self.c.fetchall()
        return rows

    # --------------------------------------------------------------
    # 1. TOP THREE ARTICLES OF ALL TIME
    # --------------------------------------------------------------
    def get_popular_articles(self):
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
        results = self.execute_query(query)

        # Print results.
        print("----------------------------------------------------------")
        print("\t\tI. TOP THREE ARTICLES OF ALL TIME")
        print("----------------------------------------------------------")
        rank = 1
        for row in results:
            print(u"  {0}. \"{1}\" — {2:,} views.".format(rank, row[0],
                  row[1]))
            rank += 1

    # --------------------------------------------------------------
    # 2. POPULAR AUTHORS OF ALL TIME
    # --------------------------------------------------------------
    def get_popular_authors(self):
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
        results = self.execute_query(query)

        # Print results.
        print("\n\n----------------------------------------------------------")
        print("\t\tII. POPULAR AUTHORS OF ALL TIME")
        print("----------------------------------------------------------")
        rank = 1
        for row in results:
            print(u"  {0}. {1} — {2:,} views.".format(rank, row[0], row[1]))
            rank += 1

    # --------------------------------------------------------------
    # 3. DAYS IN WHICH MORE THAN 1% OF REQUESTS LEAD TO ERRORS
    # --------------------------------------------------------------
    def get_days_with_errors(self):
        """Return days in which more than 1% requests lead to errors."""

        query = """
            SELECT total.day,
            ROUND(((errors.error_requests*1.0) / total.requests), 3) AS percent
            FROM (
                SELECT date_trunc('day', time) "day", count(*)
                AS error_requests
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
            WHERE
                (ROUND(((errors.error_requests*1.0)/total.requests), 3) > 0.01)
            ORDER BY percent DESC;
        """

        # Execute the above query.
        results = self.execute_query(query)

        # Print results.
        print("\n\n----------------------------------------------------------")
        print("  III. DAYS IN WHICH MORE THAN 1% OF REQUESTS LEAD TO ERRORS")
        print("----------------------------------------------------------")
        for row in results:
            date = row[0].strftime('%B %d, %Y')     # Pretty-formatting date.
            errors = str(round(row[1]*100, 1)) + "%" + " errors"
            print("   " + date + u" — " + errors)


# Print all the results.
if __name__ == '__main__':
    # Create an instance of class `LogAnalyser`.
    log = LogAnalyser()

    # Print the results.
    log.get_popular_articles()
    log.get_popular_authors()
    log.get_days_with_errors()

    log.conn.close()
