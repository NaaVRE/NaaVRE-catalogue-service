# NaaVRE-catalogue-service



## Running locally

Install dependencies

```shell
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

Start the dev database and object store:

```shell
docker compose -f dev/docker-compose.yaml up
```

Populate the dev database

```shell
while read env; do export $env; done < dev/catalogue-service.env
python app/manage.py makemigrations
python app/manage.py migrate
python app/manage.py loaddata app/fixtures.json
python app/manage.py createsuperuser --no-input
```

Run the dev server

```shell
while read env; do export $env; done < dev/catalogue-service.env
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


## Running with Docker

[//]: # (TODO: add S3 instruction or remove)

```shell
docker network create testing
docker run -d --name db --network testing -e POSTGRES_PASSWORD=fake-postgres-password postgres:17
docker run --network testing -p 127.0.0.1:8000:8000 --env-file dev/catalogue-service.env -e DB_HOST=db ghcr.io/naavre/naavre-catalogue-service:latest
```

## Deploying with Helm

Create a custom `values.yaml` file (example: [helm/naavre-catalogue-service/values-example.yaml](./helm/naavre-catalogue-service/values-example.yaml); default values: [helm/naavre-catalogue-service/values.yaml](./helm/naavre-catalogue-service/values.yaml)).

Deploy:

```shell
helm -n my-ns upgrade --install naavre-catalogue-service oci://ghcr.io/naavre/charts/naavre-catalogue-service --version v0.1.1 -f values.yaml
```