import pandas as pd
import os
import glob
from config import sparkify_dictionary
from cql import ETL
import argparse


def get_file_directory(filepath):
    """File directory where data files reside

    Arguments:
        filepath {str}

    Returns:
        str -- Absolute path of directory where data files reside
    """
    cwd = os.getcwd()
    cwd += filepath
    return cwd


def get_files(file_directory, format):
    """Retrieve list of files
    """
    return glob.glob(file_directory + f"/*.{format}")


def construct_dataframe_from_files(files):
    """Construct a pandas.DataFrame from a list of .csv files

    Returns:
        pandas.DataFrame
    """
    df = pd.concat((pd.read_csv(f) for f in files))
    df.dropna(subset=['artist'], inplace=True)
    df[['itemInSession', 'sessionId', 'userId']] = \
        df[['itemInSession', 'sessionId', 'userId']].apply(
            pd.to_numeric, downcast='integer')
    return df


def run(path, file_format):
    """Entrypoint into ETL script

    Steps:
    - Retrieve files
    - Construct a dataframe from files
    - Initialize ETL class with dictionary and dataframe
    - For each key in dictionary, create table and insert data corresponding
      to respective data in dataframe

    Arguments:
        filepath {str} -- Folder where files reside
    """
    file_directory = get_file_directory(path)
    files = get_files(file_directory, file_format)
    dataframe = construct_dataframe_from_files(files)
    etl = ETL(sparkify_dictionary, dataframe)
    for key in etl.dictionary.keys():
        etl.run(key)
        print(f"Data for {etl._table(key)} inserted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path",
        help="Filepath where files reside.  Default is '/event_data'",
        default='/event_data')
    parser.add_argument(
        "-f", "--file_format",
        help="Retrieve only files with specific format.  Default is 'csv'",
        default='csv')
    args = parser.parse_args()
    run(args.path, args.file_format)
