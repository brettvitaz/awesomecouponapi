# Awesomecouponapi

## Quick Start

A recent version of Docker is recommended to run the demo. A few scripts have been provided to get the service up and running. *These scripts must be run from the project root.*

To build the API image:

```bash
$ ./docker/build.sh
```

To start the services:

```bash
$ ./docker/deploy.sh
```

The first time the services are started, the database needs to be initialized. Please run the command:

```bash
$ ./docker/init-db.sh
```

Now the API is ready for connections. You can test it by opening the URL [http://localhost:5000/coupons](http://localhost:5000/coupons) in your browser, or using curl in your terminal:

```bash
$ curl http://localhost:5000/coupons
```

Python 3.6 is required, and a virtual environment is recommended, to run the app and unit tests locally. To run the unit tests, do something resembling the following:

```bash
$ virtualenv venv -p python3
$ source ./venv/bin/activate
$ pip install -r requirements.dev.txt
$ PYTHONPATH=. pytest tests
```

If the app is to be run locally, the file `api/config.py` must be updated to point to the database server, or an entry for `coupon-db` can be added to `/etc/hosts`.

## Stack

### API
I chose to write the service in Python because of the powerful and highly configurable web service, SQL toolkit, and serialization/validation libraries.

#### Libraries used
* Flask - for serving the API
* Waitress - for supporting multiple simultaneous connections
* SQLAlchemy - for accessing the database
* Marshmallow - for (de)serialization and validation of the input data and model objects
* Flask-SQLAlchemy - for sane connection defaults, Flask context management, Model helper methods
* Flask-Marshmallow - for the ability to create URLs for HATEOAS ready APIs and its jsonify helper method
* Marshmallow-SQLAlchemy - for allowing SQLAlchemy models to be consumed in a Marshmallow schema
* simplejson - for a better json parser
* pytest - it's a great testing framework

#### Assumptions
* A valid coupon is one where `expire_at` date is greater than or equal to `published_at`.
* This API will be consumed by an application that will parse JSON into a native object, so key order is not important.

#### Security
The API service is run by an unprivileged user. Only the API port is externally exposed.

### Database
I chose to use Postgres for the database because of its high performance, ACID compliance, and ease of use. A SQL database seemed like a good option because the data has a fixed structure, but I also considered using a NoSQL database like MongoDB to support a changing schema in the future. 

#### Security
Only the postgres connection port is shared internally to other containers through the docker network links. 

Postgres user and password can be configured at deployment time by adding them as arguments to the `deploy.sh` script:

```bash
$ ./docker/deploy.sh [postgres_user] [postgres_password]
```

A less privileged user can be used for added security. The file `api/config.py` must be updated to reflect the new auth info:

```python
SQLALCHEMY_DATABASE_URI = 'postgres://[postgres_user]:[postgres_password]@coupon-db:5432/'
```

## Considerations

### Secrets
For added security, a service like [Vault](https://www.vaultproject.io/) can be used to securely store and retrieve authentication information.

### Scale and Fault Tolerance
A container orchestration platform such as [Rancher](http://rancher.com/) can be used to manage and monitor the services. The API services may reside behind a load balancer and automatically scaled to meet demand.  

### Analytics
Access information can be collected by another service and used to determine the success of a campaign.
Error logs can be used to identify bad requests and bugs.
