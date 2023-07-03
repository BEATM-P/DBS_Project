
# README FOR DBS PROJECT

## Setup

### Requirements

todo create requirements.txt

django, djangorestframework, psycopg2-binary, postgresql

### Setting up

-Start local database with postgres

    give yourself lock file ownership    

    pg_ctl -D [absolutepathtorepo]/dbs-abgabe/bikes start

    psql bikes //check if it worked

-Run importcsv.py to initialise database with csv data

-Run django server