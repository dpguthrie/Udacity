# Project 2 - Data Modeling with Apache Cassandra

## Table of Conents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Solution](#solution)


## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

They'd like a data engineer to create an Apache Cassandra database which can create queries on song play data to answer the questions, and wish to bring you on the project. Your role is to create a database for this analysis. You'll be able to test your database by running queries given to you by the analytics team from Sparkify to create the results.

## Requirements

### ETL Pipeline Processing

1. Create `event_data_new.csv` file
2. Use appropriate datatype within the `CREATE` statement

### Data Modeling

1. Create correct Apache Cassandra tables for each of the three queries.  The `CREATE TABLE` statement should include the appropriate table
2. Demonstrate understanding of data modeling through `SELECT` statements
3. Use table names that reflect the query and result it will generate.  Table names should include alphanumeric characters and underscores, and table names must start with a letter
4. Sequence in which columns appear should reflect how the data is partitioned and the order of the data within the partitions

### Primary Keys

1. Combination of the PARTITION KEY alone or with the addition of CLUSTERING COLUMNS should be used appropriately to uniquely identify each row.

### Presentation

1. Notebook should include description of the query the data is modeled after
2. In-line comments part of project's instructions should be removed

### Extra Credit

- Add description of your PRIMARY KEY and how you arrived at the decision to use each for the query
- Use Panda dataframes to add columns to your query output

## Solution

TODO