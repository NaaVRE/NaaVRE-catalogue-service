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


## Deploying with Helm

### Prerequisite

Create a bucket in a S3-compatible object storage. Generate an access- and secret key with the following policy (replace `"BUCKET_NAME"` with the actual value):

```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ],
        "Effect": "Allow",
        "Resource": [
          "arn:aws:s3:::BUCKET_NAME",
          "arn:aws:s3:::BUCKET_NAME/*"
        ]
      }
    ]
  }
```

### Deployment

Create a custom `values.yaml` file (example: [helm/naavre-catalogue-service/values-example.yaml](./helm/naavre-catalogue-service/values-example.yaml); default values: [helm/naavre-catalogue-service/values.yaml](./helm/naavre-catalogue-service/values.yaml)).

Deploy:

```shell
helm -n my-ns upgrade --install naavre-catalogue-service oci://ghcr.io/naavre/charts/naavre-catalogue-service --version v0.1.1 -f values.yaml
```