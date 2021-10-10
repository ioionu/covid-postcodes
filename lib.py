import psycopg2
import os
import logging

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel(LOGLEVEL)

def get_connection():
    return psycopg2.connect(
        dbname=os.environ['RDS_DB_NAME'],
        user=os.environ['RDS_USERNAME'],
        password=os.environ['RDS_PASSWORD'],
        host=os.environ['RDS_HOSTNAME'],
        port=os.environ['RDS_PORT']
    )

