import psycopg2
import csv, urllib.request
import csv
import os
url = os.environ["SOURCE"]
# url = 'https://data.nsw.gov.au/data/dataset/97ea2424-abaf-4f3e-a9f2-b5c883f42b6a/resource/2776dbb8-f807-4fb2-b1ed-184a6fc2c8aa/download/confirmed_cases_table4_location_likely_source.csv'
from lib import get_connection
import os
import datetime

WINDOW = int(os.environ["WINDOW"])

query = """
insert into "case"(
    notification_date,
    postcode,
    lhd_2010_code,
    lhd_2010_name,
    lga_code19,
    lga_name19,
    likely_source_of_infection
)
values (%s, %s, %s, %s, %s, %s, %s);
"""

def load_cases():
    cut_off_date = (datetime.datetime.now() - datetime.timedelta(days=WINDOW)).date()
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    data = csv.reader(lines)
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute("truncate \"case\"")
            conn.commit()
            conn.close()
            rows = []
            for row in data:
                # print(row)
                # ['2020-01-25', '2121', 'Overseas', 'X760', 'Northern Sydney', '16260', 'Parramatta (C)']
                # TODO: much better validation.
                try:
                    d = row[0]
                    pc = int(row[1])
                    lga = int(row[5])
                except Exception as e:
                    print('issue with row')
                    continue
                if (
                    row[0] != "notification_date" and
                    datetime.date.fromisoformat(row[0]) > cut_off_date and
                    len(row[1]) > 0 and
                    len(row[2]) > 0 and len(row[3]) > 0 and len(row[4]) > 0
                ):  
                    rows.append(
                        (
                            row[0],
                            row[1],
                            row[3],
                            row[4],
                            row[5],
                            row[6],
                            row[2]
                        )
                    )

            try:
                conn = get_connection()
                with conn:
                    with conn.cursor() as curs:
                        curs.executemany(
                            query,
                            rows
                        )
                        # conn.commit()
                        # curs.close()
                        # conn.close()
            except Exception as e:
                print(e)
                pass
    return True


if __name__ == "__main__":
    load_cases()
