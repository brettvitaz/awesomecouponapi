from flask import Flask, request
from waitress import serve

import simplejson as json

from api import config
from api.importer import import_data
from api.models import db, Coupons, Stores
from api.schemas import ma, CouponsSchema


def create_app(config_module=None):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_module)

    db.init_app(flask_app)
    ma.init_app(flask_app)
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        if not Coupons.query.all():
            import_data(db)

    return flask_app


app = create_app(config)

STATUS_FILTER = {
    'invalid': Coupons.expire_at < Coupons.published_at,
    'valid': Coupons.expire_at >= Coupons.published_at,
}


@app.route('/coupons')
def route_coupons():
    """
    Returns a list of coupons.

    :arg status: Filter coupons by status.
                 Expects one of ('valid', 'invalid') 
    :return: 
    """
    coupons_schema = CouponsSchema(many=True)

    query_filter = STATUS_FILTER.get(request.args.get('status'))
    coupons_query = Coupons.query
    if query_filter is not None:
        coupons_query = coupons_query.filter(query_filter)
    try:
        coupons = coupons_query.all()
    except Exception as e:
        return json.dumps({'error': f'{e}'}), 500

    return coupons_schema.jsonify(coupons)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port='5000')
