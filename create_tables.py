import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    This function drops AWS Redshift Database tables
    Parameters
    ----------
    cur : Redshift database cursor
    conn: Redshift database connection
    """
    
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    This function creates required database tables in AWS Redshift
    Parameters
    ----------
    cur : Redshift database cursor
    conn: Redshift database connection
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''
    Connects to configured Redshift database and runs SQL queries for drop
    table operations followed by create table operations.
    The data warehouse schema is set after sucessful execution.
    '''
    # Load configuration data
    print('Loading configuration data...')
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # Connect to Redshift cluster
    print('Making connection to redshift cluster...')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    # drop database tables in they exists
    print('Drop database tables if exist...')
    drop_tables(cur, conn)
    
    # create database tables
    print("Creating database tables...")
    create_tables(cur, conn)

    # close database connection
    print("Close database connection...")
    conn.close()


if __name__ == "__main__":
    main()