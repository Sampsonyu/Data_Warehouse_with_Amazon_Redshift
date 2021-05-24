import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ARN = config.get("IAM_ROLE","ARN")
LOG_DATA = config.get("S3","LOG_DATA")
LOG_JSONPATH = config.get("S3","LOG_JSONPATH")
SONG_DATA = config.get("S3","SONG_DATA")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"


# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events(
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender  CHAR,     
    itemInSession INT,
    lastName VARCHAR,
    length FLOAT,
    level  VARCHAR, 
    location VARCHAR,
    method VARCHAR,      
    page  VARCHAR,      
    registration FLOAT,
    sessionId INT,
    song VARCHAR,
    status INT,
    ts BIGINT,  
    userAgent VARCHAR,
    userId INT
)
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs(
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    num_songs INT,
    artist_id VARCHAR,
    artist_latitude FLOAT,
    artist_longitude FLOAT,     
    artist_location VARCHAR,
    artist_name VARCHAR,
    song_id VARCHAR,
    title  VARCHAR, 
    duration FLOAT,
    year INT
)
""")

songplay_table_create = ("""
CREATE TABLE songplays(
    songplay_id INTEGER IDENTITY(1,1) NOT NULL PRIMARY KEY DISTKEY,
    start_time TIMESTAMP NOT NULL ,
    user_id INT NOT NULL,
    level VARCHAR NOT NULL,
    song_id VARCHAR, 
    artist_id VARCHAR,
    session_id BIGINT NOT NULL,
    location VARCHAR,
    user_agent VARCHAR NOT NULL
)
""")

# songplay_table_create = ("""
# CREATE TABLE songplays(
#     songplay_id INTEGER IDENTITY(1,1) NOT NULL PRIMARY KEY DISTKEY,
#     start_time TIMESTAMP NOT NULL ,
#     user_id INT NOT NULL,
#     level VARCHAR NOT NULL,
#     song_id VARCHAR, 
#     artist_id VARCHAR,
#     session_id BIGINT NOT NULL,
#     location VARCHAR,
#     user_agent VARCHAR NOT NULL
# )
# DISTSTYLE KEY
# DISTKEY (start_time)
# SORTKEY (start_time);
# """)

user_table_create = ("""
CREATE TABLE users(
    user_id VARCHAR NOT NULL PRIMARY KEY DISTKEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    gender CHAR(1) ENCODE BYTEDICT, 
    level VARCHAR ENCODE BYTEDICT
)
""")

song_table_create = ("""
CREATE TABLE songs(
    song_id VARCHAR NOT NULL PRIMARY KEY DISTKEY,
    title VARCHAR NOT NULL,
    artist_id VARCHAR NOT NULL,
    year INT NOT NULL, 
    duration FLOAT NOT NULL
)
""")

artist_table_create = ("""
CREATE TABLE artists(
    artist_id VARCHAR NOT NULL PRIMARY KEY DISTKEY,
    name VARCHAR NOT NULL,
    location VARCHAR,
    latitude FLOAT, 
    longitude FLOAT
)
""")

time_table_create = ("""
CREATE TABLE time(
    start_time TIMESTAMP NOT NULL PRIMARY KEY DISTKEY,
    hour INT NOT NULL,
    day INT NOT NULL,
    week INT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL ENCODE BYTEDICT ,
    weekday VARCHAR NOT NULL ENCODE BYTEDICT
)
""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from {}
    credentials 'aws_iam_role={}'
    json {}
    region 'us-west-2'
""").format(LOG_DATA, IAM_ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    copy staging_songs from {}
    credentials 'aws_iam_role={}'
    json 'auto'
    region 'us-west-2'
""").format(SONG_DATA, IAM_ARN)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT TIMESTAMP 'epoch' + (ts / 1000) * INTERVAL '1 Second ',
    userId,
    level,
    song_id,
    artist_id,
    sessionId,
    location,
    userAgent
FROM staging_events e
INNER JOIN staging_songs s ON e.song = s.title AND e.artist = s.artist_name
WHERE e.page = 'NextSong'
""")


user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT (userId),
           firstName,
           lastName,
           gender,
           level
    FROM staging_events
    WHERE userId IS NOT NULL;
""")


song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT(song_id),
           title,
           artist_id,
           year,
           duration
    FROM staging_songs;
""")


artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT (artist_id),
           artist_name,
           artist_location,
           artist_latitude,
           artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
""")


time_table_insert = ("""
        INSERT INTO time (start_time, hour, day, week, month, year, weekday)
        SELECT DISTINCT (TIMESTAMP 'epoch' + (ts / 1000) * INTERVAL '1 Second ') as ts_timestamp,
               EXTRACT(HOUR FROM ts_timestamp),
               EXTRACT(DAY FROM ts_timestamp),
               EXTRACT(WEEK FROM ts_timestamp),
               EXTRACT(MONTH FROM ts_timestamp),
               EXTRACT(YEAR FROM ts_timestamp),
               EXTRACT(DOW FROM ts_timestamp)
        FROM staging_events;
""")
# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
