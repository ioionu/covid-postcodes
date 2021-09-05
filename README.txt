NSW Covid Cases By Postcode

https://covid-postcodes.herokuapp.com

Add target postcodes as a parameter eg:

https://covid-postcodes.herokuapp.com/?postcodes=2015,2016,2017,2010

INSTALL

Create ".env" file:

DATABASE_HOST="localhost"
DATABASE_USER="covid"
DATABASE_PASSWORD="covid"
DATABASE_NAME="covid"
DATABASE_UPDATE_KEY="covid"
WINDOW=28
SOURCE="https://data.nsw.gov.au/data/dataset/97ea2424-abaf-4f3e-a9f2-b5c883f42b6a/resource/2776dbb8-f807-4fb2-b1ed-184a6fc2c8aa/download/confirmed_cases_table4_location_likely_source.csv"

Install requirements

pip -r requirements.txt

Create table:

cat covid.sql | psql -d covid -U covid -h localhost

TODO:

Much better validation of case data
Postcode checkboxes
Schedule fetcher
Move fetcher to bg task