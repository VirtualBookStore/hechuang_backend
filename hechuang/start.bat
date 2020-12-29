cd hechuang
rd
python .\manage.py makemigrations
python .\manage.py migrate
python .\manage.py loaddata data.yaml
python .\manage.py runserver
