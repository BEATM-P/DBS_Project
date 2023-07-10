
# README FOR DBS PROJECT

## Setup

### Requirements

todo create requirements.txt

django, djangorestframework, psycopg2-binary, postgresql

### Setting up

-Start local database with postgres

#### Linux

Initialize Database

    initdb /home/alla/Uni/dbs-abgabe/bikes 

give yourself lock file ownership

    sudo chown -R pm:pm /var/run/postgresql/

start database server

    pg_ctl -D [absolutepathtorepo]/dbs-abgabe/bikes start

open psql interactive shell

    psql postgres

Create Database for app to use

    CREATE DATABASE bikes;

Exit with Ctrl+D

-Run importcsv.py to initialise database with csv data

-Run django server
