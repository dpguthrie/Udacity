import pandas as pd
import os
import glob
import argparse

file_directory = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filepath", help="Filepath containing csv files")
args = parser.parse_args()

if args.filepath:
    file_directory += args.filepath
else:
    file_directory += '/event_data'


def get_files(file_directory):
    """Retrieve list of files
    """
    return glob.glob(file_directory + "/*.csv")


def construct_dataframe_from_files(files):
    """Construct a pandas.DataFrame from a list of .csv files

    Returns:
        pandas.DataFrame
    """
    df = pd.concat((pd.read_csv(f) for f in files))
    df.dropna(subset=['artist'], inplace=True)
    df[['itemInSession', 'sessionId', 'userId']] = \
        df[['itemInSession', 'sessionId', 'userId']].apply(pd.to_numeric)
    return df
