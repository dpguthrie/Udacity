import os
import glob
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import sql_queries


artist_data = []
song_data = []
user_data = []
time_data = []
songplay_data = []

insert_data = [
    (sql_queries.artist_table_insert, artist_data),
    (sql_queries.song_table_insert, song_data),
    (sql_queries.user_table_insert, user_data),
    (sql_queries.time_table_insert, time_data),
    (sql_queries.songplay_table_insert, songplay_data)
]


def process_song_file(cur, filepath):
    """
    Reads current song file and appends data to appropriate lists

    Parameters
    ----------
    cur: psycopg2.connect.cursor
        Execute PostgreSQL command in database session
    filepath:  str
        Reference to file containing data to process
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # convert NaN to None
    df = df.where(pd.notnull(df), None)

    # insert artist record first, as it is referenced in songs table
    artist_data.append((df[['artist_id', 'artist_name', 'artist_location',
                       'artist_latitude', 'artist_longitude']].values[0]))

    # insert song record
    song_data.append(
        (df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0]))


def process_log_file(cur, filepath):
    """
    Reads current log file and appends data to appropriate lists

    Parameters
    ----------
    cur: psycopg2.connect.cursor
        Execute PostgreSQL command in database session
    filepath:  str
        Reference to file containing data to process
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')

    for _, row in df.iterrows():

        # Append data to appropriate lists
        time_data.append((
            row.ts, row.ts.hour, row.ts.day, row.ts.week,
            row.ts.month, row.ts.year, row.ts.weekday()))
        user_data.append(
            (row.userId, row.firstName, row.lastName, row.gender, row.level))

        # See if BOTH song and artist exist
        cur.execute(
            sql_queries.song_select, (row.song, row.artist, row.length))
        songplay_results = cur.fetchone()

        # Assign ids to results or None
        song_id, artist_id = \
            songplay_results if songplay_results else None, None
        songplay_data.append((
            row.ts, row.userId, row.level, row.sessionId, row.location,
            row.userAgent, song_id, artist_id))


def process_data(cur, conn, filepath, func):
    """
    This function will loop through a series of files (either song or long)
    and then each file will be passed to a function specified as an argument

    Parameters
    ----------
    cur: psycopg2.connect.cursor
        Execute PostgreSQL command in database session
    conn:  psycopg2.connect
        Handles connection to a PostgreSQL database instance
    filepath:  str
        Reference to folder containing one or more files
    func: function
        Either process_song_file or process_log_file
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """Function to call that will run the entire ETL process
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    for insert_tuple in insert_data:
        execute_values(cur, insert_tuple[0], insert_tuple[1])

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
