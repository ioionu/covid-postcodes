from lib import get_connection, logger

query = """
CREATE TABLE public."case" (
    notification_date date NOT NULL,
    postcode character varying,
    lhd_2010_code character varying(4),
    lhd_2010_name character varying(21),
    lga_code19 integer,
    lga_name19 character varying(33)
);
"""

def create_db():
    """
    Create Empty Case Database.
    """
    logger.info("Creating Database")
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute(query)
            conn.commit()

if __name__ == "__main__":
    create_db()
