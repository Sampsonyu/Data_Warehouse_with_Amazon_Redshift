# Data_warehouse_with_Amazon_Redshift

## Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. Their analytics team is particularly interested in understanding what songs users are listening to. Their user base and song database has grown and want to move their processes and data onto the cloud. 

## Project Description

The goal of this project is to develop a data model and ETL process for song play analysis.

Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. ETL pipeline has to be built that extracts data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to finding insights.

Staging tables, facts and dimension tables are to be defined in star schema using Amazon Redshift.

ETL pipelines that transfers data from files in json format to Amazon Redshift database are to be developed using python.

## Datasets

Data is available in two separate folders in s3 under log_data and song_data folders.

### Source File Information:
There are 2 different types of Data (Event Files and Song Files) that is available for the Sparkify music streaming application amd they are stored as JSON files. Following are the paths for the files:

**Song Data**
s3://udacity-dend/song_data

**Log Data** 
s3://udacity-dend/log_data

Following are the JSON file structures:


- Song Files: It has all Songs, Albums and Artist related details. Here is one sample row:
        {   "num_songs": 1, 
            "artist_id": "ARD7TVE1187B99BFB1", 
            "artist_latitude": null, 
            "artist_longitude": null, 
            "artist_location": "California - LA", 
            "artist_name": "Casual", 
            "song_id": "SOMZWCG12A8C13C480", 
            "title": "I Didn't Mean To", 
            "duration": 218.93179, 
            "year": 0
        }

- Log Files: It has the logs of the user's music listening activity on the app. Here is one sample row:
        {   "artist":null,
            "auth":"Logged In",
            "firstName":"Walter",
            "gender":"M",
            "itemInSession":0,
            "lastName":"Frye",
            "length":null,
            "level":"free",
            "location":"San Francisco-Oakland-Hayward, CA",
            "method":"GET",
            "page":"Home",
            "registration":1540919166796.0,
            "sessionId":38,
            "song":null,
            "status":200,
            "ts":1541105830796,
            "userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"
        }
        

### Requirements

You'll need an [AWS](https://aws.amazon.com/) account with the resources to provision a Redshift cluster (recommended: 4 x dc2.large EC2 instances)

You'll also need this software installed on your system 
* [PostgreSQL](https://www.postgresql.org/download/)
* [Python](https://www.python.org/downloads/)

In addition you'll need the PostgreSQL python driver which can be obtained via `pip`
```
pip install psycopg2 
```

## Database Schema

 The schema design used for this project is star schema with one fact table and four dimension tables
 
 Star Schema is suitable for this analysis because:
 - The data will de normalized and it helps in faster reads
 - Queries will be simpler and better performing as there are lesser joins
 - We don't have any many to many relationships

![Sparkify star schema](https://github.com/Sampsonyu/Data_warehouse_with_Amazon_Redshift/blob/main/sparkify_erd.png)

### Staging Tables
**staging_events** - Used as interim table for log data before data is logged into analytical tables. All the data from log_data folder is loaded into this table and then moved into facts and dimensions as per the rules.
**staging_songs** - Used as interim table for song data before data is logged into analytical tables. All the data from song_data folder is loaded into this table and then moved into facts and dimensions as per the rules.

### Fact Table
**songplays** -  Records log data associated with song plays (records with page NextSong). songplays table uses distribution style as KEY and the distribution key and sort key is start_time. Using this rows with similar values are placed int the same slice as our time dimension can grow real big.

### Dimension Tables
**users** - users in the app (user_id, first_name, last_name, gender, level). users table uses distribution style as AUTO and sortkey is user_id. Using this Redshift intelligently takes care of distribution depending on the data size, data is sorted by user_id in the table

**songs** - songs in music database (song_id, title, artist_id, year, duration). songs table uses distribution style as AUTO and sortkey is song_id. Using this Redshift intelligently takes care of distribution depending on the data size, data is sorted by song_id in the table

**artists** - artists in music database (artist_id, name, location, latitude, longitude). artists table uses distribution style as AUTO and sortkey is artist_id. Using this Redshift intelligently takes care of distribution depending on the data size, data is sorted by artist_id in the table

**time** - timestamps of records in songplays broken down into specific units (start_time, hour, day, week, month, year, weekday). time table uses distribution style as KEY and the distribution key and sort key is start_time. Using this rows with similar values are placed int the same slice as our time dimension can grow real big.

## Project Structure

```
sparkify-redshift-dwh/
 ├── README.md              Documentation of the project
 ├── create_tables.py       Python script to create all tables in Redshift
 ├── dwh.cfg                Configuration file for setting up S3 sources & Redshift credentials
 ├── etl.py                 Python script to load data from S3 into Redshift and again into the datawarehouse
 └── sql_queries.py         Python file containing all SQL statements for ELT process
```

### Quick Start

Provision a Redshift cluster within AWS utilizing either the Quick Launch wizard, [AWS CLI](https://docs.aws.amazon.com/cli/index.html), or the various AWS SDKs (e.g. [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for python).

Update the credentials and configuration details in `dwh.cfg`. Change the S3 source bucket locations if necessary.

Create the database tables by running the `create_tables.py` script, followed by `etl.py` to perform the data loading.

```
$ python create_tables.py 
$ python etl.py
```
Optionally a PostgreSQL client (or `psycopg2`) can be used to connect to the Sparkify db to perform analytical queries afterwards.


## Example Analytical Queries

- **Top Ten most played songs:** <br>
    SELECT s.title, count(sp.songplay_id) play_count <br>
    FROM songplays sp, songs s <br>
    WHERE sp.song_id = s.song_id <br>
    GROUP BY s.title <br>
    ORDER BY play_count DESC <br>
    LIMIT 10; <br>
    
- **Top ten locations with most song play count:** <br>
    SELECT sp.location, count(sp.songplay_id) play_count <br>
    FROM songplays sp <br>
    GROUP BY sp.location <br>
    ORDER BY play_count DESC <br>
    LIMIT 10; <br>

- **User counts by Level:** <br>
    SELECT u.level, count(u.user_id) user_count <br>
    FROM users u <br>
    GROUP BY u.level;
