from flask import Flask, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from waitress import serve

from api import config
from api.importer import import_data
from api.models import db, Coupons
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

    :query status: Filter coupons by status.
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
        return coupons_schema.jsonify(coupons)

    except SQLAlchemyError as e:
        return jsonify(error=f'{e}'), 500


@app.route('/coupons/<int:coupon_id>', methods=['GET', 'PUT', 'DELETE'])
def route_coupons_by_id(coupon_id):
    coupon_schema = CouponsSchema()

    try:
        coupon = Coupons.query.get_or_404(coupon_id)

    except SQLAlchemyError as e:
        return jsonify(error=f'{e}'), 500

    if request.method == 'GET':
        return coupon_schema.jsonify(coupon)

    if request.method == 'PUT':
        coupon_update, errors = coupon_schema.load(request.json, instance=coupon)

        if errors:
            return jsonify(error=errors), 400

        try:
            db.session.add(coupon_update)
            db.session.commit()
            return coupon_schema.jsonify(coupon_update)

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify(error=f'{e}'), 500

    if request.method == 'DELETE':
        try:
            db.session.delete(coupon)
            db.session.commit()
            return '', 204

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify(error=f'{e}'), 500


@app.route('/coupons', methods=['POST'])
def route_add_coupon():
    coupon_schema = CouponsSchema()

    coupon, errors = coupon_schema.load(request.json)
    if errors:
        return jsonify(error=errors), 400

    try:
        db.session.add(coupon)
        db.session.commit()
        return jsonify(id=coupon.id)

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(error=f'{e}')


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port='5000')
