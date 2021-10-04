from flask import Flask, request, jsonify, render_template, abort
from flask.json import JSONEncoder
from werkzeug.exceptions import BadRequest
import datetime
import psycopg2
import os
from load_cases import load_cases
from create_db import create_db
from lib import get_connection

# Number of days to query back from today.
WINDOW = int(os.environ["WINDOW"])

app = Flask(__name__)

query = """
select dr.d, unlinked.total as unlinked_total, linked.total as linked_total
FROM
    (
        SELECT d::date from generate_series(date %s, date %s, '1 day') as gs(d)
    ) dr
left join
    (
        select notification_date, coalesce(count(notification_date),0) as total from public."case"
        where
            not likely_source_of_infection = 'Locally acquired - linked to known case or cluster' and
            postcode in %s
        group by notification_date
    ) unlinked
on dr.d = unlinked.notification_date
left join
    (
        select notification_date, coalesce(count(notification_date),0) as total from public."case"
        where
            likely_source_of_infection = 'Locally acquired - linked to known case or cluster' and
            postcode in %s
        group by notification_date
    ) linked
on dr.d = linked.notification_date
"""

postcode_query = """
select distinct  postcode, lga_name19 from \"case\" order by lga_name19;
"""


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

@app.route('/api/v1/cases', methods=['POST'])
def get_data():
    if (request.is_json):
        conn = get_connection()
        with conn:
            with conn.cursor() as curs:
                post = request.get_json()
                if 'postcodes' not in post:
                    abort(400, description="postcodes not found")
                postcodes = tuple(
                    [str(int(postcode)) for postcode in post['postcodes']]
                )
                end = datetime.datetime.now()
                start = end - datetime.timedelta(days=WINDOW)
                curs.execute(
                    query,
                    (
                        start.date(),
                        end.date(),
                        postcodes,
                        postcodes
                    )
                )
                results = curs.fetchall()
                return jsonify(results)

@app.route('/api/v1/postcodes', methods=['GET'])
def get_postcodes():
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute(postcode_query)
            results = curs.fetchall()
            return jsonify(results)

@app.route('/loadcases', methods=['GET'])
def case_loader():
    if (
        "DATABASE_UPDATE_KEY" in os.environ and
        "key" in request.args and
        request.args.get('key') == os.environ['DATABASE_UPDATE_KEY']
    ):
        load_cases()
        return "Cases loading"
    return abort(500, "Key error")

@app.route('/install', methods=['GET'])
def installer():
    if (
        "DATABASE_UPDATE_KEY" in os.environ and
        "key" in request.args and
        request.args.get('key') == os.environ['DATABASE_UPDATE_KEY']
    ):
        create_db()
        return "DB installed"
    return abort(500, "Key error")


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)