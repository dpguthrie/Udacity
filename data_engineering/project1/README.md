Data Engineering - Project 1
============================

Summary
-------

The purpose of this project is to create data models (represented as tables in a PostgreSQL database) that represent Sparkify's data collected from their music streaming service.  Additionally, after creating the tables in the database, an ETL process is developed that moves data from JSON files (where they're unable to be analyzed) to the appropriate tables in the PostgreSQL database.

Run Scripts
-----------

First, you want to make sure that the tables exist in the database.  Run the following command::

    $ python create_tables.py

Second, run the ETL script to transfer data from the json files to the newly created tables::

    $ python etl.py

Additional Files
----------------

### Jupyter Notebooks

- Analysis.ipynb:  Analyze some of the data per Sparkify's stated objective
- test.ipynb:  Test whether or not data is actually getting into the database

### Python

- create_tables.py:  Connect to database and create tables specified in sql_queries.py
- sql_queries.py:  SQL statements to execute (CREATE, INSERT, SELECT)
- etl.py:  Functions utilized to extract, transform, and load data from json to postgresql
