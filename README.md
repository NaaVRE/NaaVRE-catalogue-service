# NaaVRE-catalogue-service

## Running locally

Install dependencies

```shell
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

Setup the dev database

```shell
python app/manage.py makemigrations
python app/manage.py migrate
python app/manage.py loaddata app/fixtures.json
python app/manage.py createsuperuser
```

Run the dev server

```shell
while read env; do export $env; done < dev.env
python app/manage.py runserver
```

API testing is done with [bruno](https://github.com/usebruno/bruno), and the collection in the [./bruno](./bruno) folder.
