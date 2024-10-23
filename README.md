# NaaVRE-catalogue-service

## Running locally

Install dependencies

```shell
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

Start the dev database

```shell
docker run -d -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=fake-postgres-password --name naavre-catalogue-db postgres:17
```

Populate the dev database

```shell
while read env; do export $env; done < dev.env
python app/manage.py makemigrations
python app/manage.py migrate
python app/manage.py loaddata app/fixtures.json
python app/manage.py createsuperuser --no-input
```

Run the dev server

```shell
while read env; do export $env; done < dev.env
python app/manage.py runserver
```

API testing is done with [bruno](https://github.com/usebruno/bruno), and the collection in the [./bruno](./bruno) folder.

To run the API test from the command line:

```shell
npm install
cd bruno
bru run --env localhost
```

(Optional) To reset the dev database, run `docker stop naavre-catalogue-db` and `docker rm naavre-catalogue-db`, then
follow the steps starting from “Start the dev database”.
