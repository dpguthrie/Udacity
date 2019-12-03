# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE songplays (
    songplay_id SERIAL PRIMARY KEY,
    start_time timestamp REFERENCES time(start_time),
    user_id int NOT NULL,
    level char (4) NOT NULL,
    song_id varchar REFERENCES songs(song_id),
    artist_id varchar REFERENCES artists(artist_id),
    session_id int NOT NULL,
    location varchar (125),
    user_agent varchar (255) NOT NULL
)
""")

user_table_create = ("""
CREATE TABLE users (
    user_id int PRIMARY KEY,
    first_name varchar (75) NOT NULL,
    last_name varchar (75) NOT NULL,
    gender char (1),
    level char (4) NOT NULL
)
""")

song_table_create = ("""
CREATE TABLE songs (
    song_id varchar PRIMARY KEY,
    title varchar NOT NULL,
    artist_id varchar REFERENCES artists(artist_id),
    year int,
    duration float
)
""")

artist_table_create = ("""
CREATE TABLE artists (
    artist_id varchar PRIMARY KEY,
    name varchar NOT NULL,
    location varchar (125),
    latitude float,
    longitude float
)
""")

time_table_create = ("""
CREATE TABLE time (
    start_time timestamp NOT NULL,
    hour int NOT NULL,
    day int NOT NULL,
    week int NOT NULL,
    month int NOT NULL,
    year int NOT NULL,
    weekday int NOT NULL
)
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (
    start_time, user_id, level, session_id, location,
    user_agent, song_id, artist_id)
VALUES %s
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES %s
ON CONFLICT (user_id) DO UPDATE
    SET level = EXCLUDED.level
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES %s
ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES %s
ON CONFLICT (artist_id) DO NOTHING
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES %s
""")

# FIND SONGS

song_select = ("""
SELECT A.song_id, A.artist_id
FROM songs A
JOIN artists B ON A.artist_id = B.artist_id
WHERE A.title = %s AND B.name = %s AND A.duration = %s
""")

# ANALYTICAL QUERIES

top_artists_select = ("""
SELECT artists.name, COUNT(*)
FROM songplays
JOIN artists ON songplays.artist_id = artists.artist_id
GROUP BY artists.name
ORDER BY COUNT(*) DESC
""")

top_songs_select = ("""
SELECT songs.title, COUNT(*)
FROM songplays
JOIN songs ON songplays.song_id = songs.song_id
GROUP BY songs.title
ORDER BY COUNT(*) DESC
""")


# QUERY LISTS

create_table_queries = [
    user_table_create, artist_table_create, song_table_create,
    songplay_table_create, time_table_create]
drop_table_queries = [
    songplay_table_drop, user_table_drop, song_table_drop,
    artist_table_drop, time_table_drop]
