# NSW Covid Cases By Postcode

https://covid-postcodes.herokuapp.com

Add target postcodes as a parameter eg:

https://covid-postcodes.herokuapp.com/?postcodes=2015,2016,2017,2010

## INSTALL

Create ".env" file:

```TXT
RDS_HOSTNAME="localhost"
RDS_PORT="5432"
RDS_DB_NAME="covid"
RDS_USERNAME="covid"
RDS_PASSWORD="covid"
WINDOW=28
SOURCE="https://data.nsw.gov.au/data/dataset/97ea2424-abaf-4f3e-a9f2-b5c883f42b6a/resource/2776dbb8-f807-4fb2-b1ed-184a6fc2c8aa/download/confirmed_cases_table4_location_likely_source.csv"
```

### Install requirements

pip -r requirements.txt

### Create table

```
http://localhost/install?key=${DATABASE_UPDATE_KEY}
```

### Fetch case data

```
http://localhost/loadcases?key=${DATABASE_UPDATE_KEY}
```

## TODO:

 - Build a postcode selector map
 - Much better validation of case data
 - Schedule fetcher
 - Move fetcher to bg task
