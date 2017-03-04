# Awesomecouponapi

## Stack

I chose to write the service in Python because of the powerful and highly configurable web service, sql toolkit, and serialization/validation libraries.

I chose to use Postgres for the database because of its high performance, ACID compliance, and ease of use. A SQL database seemed like a good option because the data has a fixed structure, but I also considered using a NoSQL database like MongoDB to support a changing schema in the future. 

## API
### Libraries used
* Flask - for serving the API
* Waitress - for supporting multiple simultaneous connections
* SQLAlchemy - for accessing the database
* Marshmallow - for (de)serialization and validation of the input data and model objects
* Flask-SQLAlchemy - for sane connection defaults, Flask context management, Model helper functions
* Flask-Marshmallow - for the ability to create urls for HATEOAS ready APIs and its jsonify method
* Marshmallow-SQLAlchemy - for allowing SQLAlchemy models to be consumed in a Marshmallow schema
* simplejson - for a better json parser
* pytest - it's a great testing framework

### Assumptions
* A valid coupon is one where expire_at date is less than or equal to published_at

## Database
### Security
Ports are only shared internally through the docker network links. Username and password can be configured at deployment time. 

## Considerations
* Implement secrets using a service like Vault
* Scale api service

## TODO
* Tests
* flask blueprints?
