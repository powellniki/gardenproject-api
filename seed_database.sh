#!/bin/bash

rm db.sqlite3
rm -rf ./gardenapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations gardenapi
python3 manage.py migrate gardenapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata gardeners
python3 manage.py loaddata posts
python3 manage.py loaddata topics
# python3 manage.py loaddata posttopics
# python3 manage.py loaddata comments

