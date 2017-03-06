from flask import Flask, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from waitress import serve
from werkzeug import exceptions

from api import config
from api.importer import import_data
from api.models import db, Coupons
from api.schemas import ma, CouponsSchema


def create_app(config_module=None):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_module)

    return flask_app


def init_app(flask_app):
    db.init_app(flask_app)
    ma.init_app(flask_app)


def init_db(do_import=True):
    db.drop_all()
    db.create_all()
    if do_import:
        import_data(db)


app = create_app(config)

FILTERS = {
    'status': {
        'invalid': Coupons.expire_at < Coupons.published_at,
        'valid': Coupons.expire_at >= Coupons.published_at,
    }
}

coupons_schema = CouponsSchema(many=True)
coupon_schema = CouponsSchema()


@app.route('/coupons')
def route_coupons():
    """Returns a list of coupons.

    :query status: Filter coupons by status.
                   Expects one of ('valid', 'invalid') 

    :raises: werkzeug.exceptions.BadRequest, sqlalchemy.SQLAlchemyError                  
    :rtype: flask.Response
    """
    coupons_query = Coupons.query

    # Apply filters to query and warn user of invalid arguments
    invalid_args = []
    for arg, value in request.args.items():
        if FILTERS.get(arg, {}).get(value) is not None:
            coupons_query = coupons_query.filter(FILTERS[arg].get(value))
        else:
            invalid_args.append(f'{arg}={value}')

    if invalid_args:
        raise exceptions.BadRequest(f'Invalid arguments: {invalid_args}')

    coupons = coupons_query.all()
    return coupons_schema.jsonify(coupons)


def assert_content_type():
    """Assert that the Content-Type is :mimetype:`application/json`.

    :raises: werkzeug.exceptions.UnsupportedMediaType
    """
    if not request.is_json:
        raise exceptions.UnsupportedMediaType(f"Expected Content-Type: 'application/json'; "
                                              f"got: '{request.headers.environ.get('CONTENT_TYPE')}'")


@app.route('/coupons/<coupon_id>', methods=['GET', 'PUT', 'DELETE'])
def route_coupons_by_id(coupon_id):
    """Retrieves a coupon by id first and then perform HTTP method specific action.
    
    :param coupon_id: Id of coupon. Must be a positive integer. 
    :type coupon_id: int
    
    :raises: werkzeug.exceptions.BadRequest, sqlalchemy.SQLAlchemyError
    :rtype: flask.Response
    """
    # Validate coupon id is a positive integer
    try:
        if int(coupon_id) < 1:
            raise ValueError()
    except ValueError:
        raise exceptions.BadRequest(f"Coupon ID must be an positive integer; got '{coupon_id}'")

    # Retrieve the coupon from the database (or return 404)
    coupon = Coupons.query.get_or_404(coupon_id)

    if request.method == 'GET':
        # Return the selected coupon
        return coupon_schema.jsonify(coupon)

    if request.method == 'PUT':
        assert_content_type()

        # Use the coupon schema to validate json data and merge with the retrieved coupon
        coupon_update, errors = coupon_schema.load(request.json, instance=coupon)

        if errors:
            raise exceptions.BadRequest(errors)

        # Update the selected coupon and return it
        db.session.add(coupon_update)
        db.session.commit()
        return coupon_schema.jsonify(coupon_update)

    if request.method == 'DELETE':
        # Delete the selected coupon and return no response
        db.session.delete(coupon)
        db.session.commit()
        return '', 204


@app.route('/coupons', methods=['POST'])
def route_add_coupon():
    """Add a coupon.
    
    Request Content-Type must be :mimetype:`application/json` or operation will fail.
    
    :raises: werkzeug.exceptions.BadRequest, sqlalchemy.SQLAlchemyError
    :rtype: flask.Response
    """
    assert_content_type()

    # Use coupon schema to validate json data and create the coupon item
    coupon, errors = coupon_schema.load(request.json)
    if errors:
        raise exceptions.BadRequest(errors)

    db.session.add(coupon)
    db.session.commit()
    return jsonify(id=coupon.id), 201, {'Location': f'/coupons/{coupon.id}'}


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(415)
def error_bad_request(e):
    return log_and_jsonify(e.description, e.code)


@app.errorhandler(500)
def error_internal_server_error(e):
    if isinstance(e, exceptions.HTTPException):
        return log_and_jsonify(e.description, e.code)
    return log_and_jsonify(str(e), 500)


@app.errorhandler(SQLAlchemyError)
def error_sql_alchemy_error(e):
    db.session.rollback()
    return log_and_jsonify(repr(e), 500)


def log_and_jsonify(message, code):
    app.logger.warn(message, extra={'method': request.method, 'url': request.path})
    return jsonify(error=message), code


if __name__ == '__main__':
    init_app(app)

    import sys
    if 'init' in sys.argv:
        with app.app_context():
            init_db()
        exit(0)

    from api.logs import file_handler
    app.logger.addHandler(file_handler)

    serve(app, host='0.0.0.0', port='5000')
