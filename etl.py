import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

def load_staging_tables(cur, conn):
    ''' 
    Load data from S3 into staging tables within the data warehouse.
    Args:
        cur : cursor for current sql connection
        conn : a psycopg2 db connection
    '''
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

def insert_tables(cur, conn):
    ''' 
    Execute insert table SQL commands against the staging tables
    for insertion into fact and dimensional tables.
    Args:
        cur : cursor for current sql connection
        conn : a psycopg2 db connection
    '''
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''
    Connects to configured Redshift database and loads data from S3
    and further transforms it into fact and dimensional tables.
    The data warehouse is fully populated after sucessful execution.
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()