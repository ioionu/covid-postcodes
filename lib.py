import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname=os.environ['DATABASE_NAME'],
        user=os.environ['DATABASE_USER'],
        password=os.environ['DATABASE_PASSWORD'],
        host=os.environ['DATABASE_HOST']
    )