import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """Creates database if it does not exist

    Returns
    -------
    cur: psycopg2.connect.cursor
    conn:  psycopg2.connect
    """

    # connect to default database
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute(
        "CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    Drop the tables specified in the list drop_table_queries, which
    can be found in the create_tables.py file

    Parameters
    ----------
    cur: psycopg2.connect.cursor
        Execute PostgreSQL command in database session
    conn:  psycopg2.connect
        Handles connection to a PostgreSQL database instance
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """Create the tables specified in the list create_table_queries, which
       can be found in the create_tables.py file

    Parameters
    ----------
    cur: psycopg2.connect.cursor
        Execute PostgreSQL command in database session
    conn:  psycopg2.connect
        Handles connection to a PostgreSQL database instance
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """Function to call that will run the entire create database / tables process
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
