from flask_marshmallow import Marshmallow

from api.models import Coupons, Stores

ma = Marshmallow()


class CouponsSchema(ma.ModelSchema):
    store = ma.Nested('StoresSchema', exclude=('id',))

    class Meta:
        model = Coupons


class StoresSchema(ma.ModelSchema):
    class Meta:
        model = Stores
