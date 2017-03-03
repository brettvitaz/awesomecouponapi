import simplejson as json

from api.schemas import CouponsSchema

coupons_schema = CouponsSchema(many=True)


def import_data(db):
    print('importing...')
    with open('coupons.json') as f:
        j = json.load(f)
        coupon = coupons_schema.load(j)
        try:
            db.session.add_all(coupon.data)
            db.session.commit()
        finally:
            db.session.close()
