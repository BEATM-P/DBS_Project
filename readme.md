
# README FOR DBS PROJECT

## Setup

### Linux

- install dependencies (consider doing this in a venv)

        pip install -r requriements.txt

- install postgres for your platform

- Initialize Database

        initdb /home/alla/Uni/dbs-abgabe/bikes

- give yourself lock file ownership

        sudo chown -R pm:pm /var/run/postgresql/

- start database server

        pg_ctl -D [absolutepathtorepo]/dbs-abgabe/bikes start

- open psql interactive shell

        psql postgres

- Create Database for app to use

        CREATE DATABASE bikes;

- Exit with Ctrl+D

- Run init_database.py to initialise database with csv data

- Run main.py, which starts the Dash server
