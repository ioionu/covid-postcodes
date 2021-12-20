# NSW Covid Cases By Postcode

http://covid-dev.eba-kpgmesnz.ap-southeast-2.elasticbeanstalk.com

Add target postcodes as a parameter eg:

http://covid-dev.eba-kpgmesnz.ap-southeast-2.elasticbeanstalk.com/?postcodes=2015,2016,2017,2010

## INSTALL

Create ".env" file:

```TXT
RDS_HOSTNAME="localhost"
RDS_PORT="5432"
RDS_DB_NAME="covid"
RDS_USERNAME="covid"
RDS_PASSWORD="covid"
WINDOW=28
LOGLEVEL=WARN
SOURCE="https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2-f52778048b29/download/confirmed_cases_table1_location.csv"
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
