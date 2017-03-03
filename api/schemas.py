from flask_marshmallow import Marshmallow

from api.models import Coupons, Stores

ma = Marshmallow()


def serialize_datetime(obj, key):
    return f"{getattr(obj, key).isoformat(timespec='milliseconds')}Z"


class CouponsSchema(ma.ModelSchema):
    expire_at = ma.Function(deserialize=lambda obj: obj,
                            serialize=lambda obj: serialize_datetime(obj, 'expire_at'))
    published_at = ma.Function(deserialize=lambda obj: obj,
                               serialize=lambda obj: serialize_datetime(obj, 'published_at'))
    store = ma.Nested('StoresSchema', exclude=('id',))

    class Meta:
        model = Coupons


class StoresSchema(ma.ModelSchema):
    class Meta:
        model = Stores
