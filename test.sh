rm db.sqlite3
python3 manage.py makemigrations LegacySite
python3 manage.py makemigrations
python3 manage.py migrate
sh import_dbs.sh

python3 manage.py test
