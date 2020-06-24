init:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt

database:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py format_csv
	python manage.py import_csv
