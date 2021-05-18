# Data_warehouse_with_Amazon_Redshift

## Purpose
This database serves analytical data repository for Sparkify, a startup which building a new music streaming application. They intend to perform analytics on understand the listening habits of their users. Ideally, the want to know which users are playing certain songs and further gather all relevant metadata about the track played. Currently all their data is stored in Amazon S3, and will copy their data over to Redshift for analysis.

## Setup

### Requirements

You'll need an [AWS](https://aws.amazon.com/) account with the resources to provision a Redshift cluster (recommended: 4 x dc2.large EC2 instances)

You'll also need this software installed on your system 
* [PostgreSQL](https://www.postgresql.org/download/)
* [Python](https://www.python.org/downloads/)

In addition you'll need the PostgreSQL python driver which can be obtained via `pip`
```
pip install psycopg2 
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

## Project Structure

```
sparkify-redshift-dwh/
 ├── README.md              Documentation of the project
 ├── create_tables.py       Python script to create all tables in Redshift
 ├── dwh.cfg                Configuration file for setting up S3 sources & Redshift credentials
 ├── etl.py                 Python script to load data from S3 into Redshift and again into the datawarehouse
 └── sql_queries.py         Python file containing all SQL statements for ELT process
```
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
