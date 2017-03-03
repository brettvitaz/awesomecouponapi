import simplejson as json

from api.schemas import ma, CouponsSchema


class CouponsImportSchema(CouponsSchema):
    expire_at = ma.String()
    published_at = ma.String()


coupons_schema = CouponsImportSchema(many=True)


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
