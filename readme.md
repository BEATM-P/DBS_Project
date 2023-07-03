
# README FOR DBS PROJECT

## Setup

### Requirements

todo create requirements.txt

django, djangorestframework, psycopg2-binary, postgresql

### Setting up

-Create local database with postgres

    Database should be in default path, not in repo as postgres will not recognize it otherwise (mb we can add the repo to postgres path but idk)

    give superuser access to your user

    put md5 in the first two lines of /var/lib/pgsql/data/pg_hba.conf

-Run importcsv.py to initialise database with csv data

-Run django server
