import psycopg2
import csv, urllib.request
import csv
import os
from lib import get_connection, logger
import os
import datetime

WINDOW = int(os.environ["WINDOW"])
url = os.environ["SOURCE"]
print_row_error = False

query = """
insert into "case"(
    notification_date,
    postcode,
    lhd_2010_code,
    lhd_2010_name,
    lga_code19,
    lga_name19
)
values (%s, %s, %s, %s, %s, %s);
"""

def load_cases():
    logger.info("Loading cases")
    cut_off_date = (datetime.datetime.now() - datetime.timedelta(days=WINDOW)).date()

    logger.info("Fetching cases from {url}".format(url=url))
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    data = csv.reader(lines)
    rows = []
    error_count = 0

    logger.info(
        "Removing cases from before {cut_off_date} and validating {count} rows".format(
            cut_off_date=cut_off_date,
            count=len(lines)
        )
    )

    for row in data:

        # Skip csv header and dates outsout target window.
        if (
            row[0] == "notification_date" or
            datetime.date.fromisoformat(row[0]) < cut_off_date
        ):
            continue

        # Note: CSV format.
        # ['2020-01-25', '2134', 'X700', 'Sydney', '11300', 'Burwood (A)']


        # Make sure integers are integers before we try insert.
        # TODO: *much* better validation.
        try:
            pc = int(row[1])
            lga = int(row[5])
        except Exception as e:
            if print_row_error:
                logger.warn('issue with row')
                logger.warn(row)
                logger.warn(e.__str__())
            error_count = error_count+1
            continue
        rows.append(
            (
                row[0],
                row[1],
                row[3],
                row[4],
                row[5],
                row[6]
            )
        )

    row_count = len(rows)
    n = 500
    rows=[rows[i:i + n] for i in range(0, len(rows), n)]

    try:
        conn = get_connection()
        curs = conn.cursor()

        logger.info("Truncating existing records")
        curs.execute("truncate \"case\"")

        logger.info("Loading {row_count} cases.".format(row_count=row_count))
        for chunk in rows:
            curs.executemany(
                query,
                chunk
            )
        conn.commit()
        conn.close()
        logger.info(
            'Fetch completed. {row_count} saved to DB. {error_count} cases skipped.'.format(
                row_count=row_count,
                error_count=error_count
            )
        )
    except Exception as e:
        logger.error("Error while saving")
        logger.error(e)

if __name__ == "__main__":
    load_cases()
