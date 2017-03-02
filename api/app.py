from flask import Flask
from waitress import serve

from api import config
from api.importer import import_data
from api.models import db, Coupons, Stores
from api.schemas import ma, CouponsSchema, StoresSchema


def create_app(config_module=None):
    app = Flask(__name__)
    app.config.from_object(config_module)

    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        if not Coupons.query.all():
            import_data(db)

    return app


app = create_app(config)


@app.route('/')
def route_root():
    return 'Coupon API'


serve(app, host='0.0.0.0', port='5000')
