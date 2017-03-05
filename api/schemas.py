from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError

from api.models import Coupons, Stores

ma = Marshmallow()


def deserialize_datetime(obj):
    try:
        return datetime.strptime(obj, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError as e:
        raise ValidationError(str(e))


def serialize_datetime(obj, key):
    return f"{getattr(obj, key).isoformat(timespec='milliseconds')}Z"


class CouponsSchema(ma.ModelSchema):
    expire_at = ma.Function(deserialize=lambda obj: deserialize_datetime(obj),
                            serialize=lambda obj: serialize_datetime(obj, 'expire_at'))
    published_at = ma.Function(deserialize=lambda obj: deserialize_datetime(obj),
                               serialize=lambda obj: serialize_datetime(obj, 'published_at'))
    store = ma.Nested('StoresSchema', exclude=('id',))

    class Meta:
        model = Coupons


class StoresSchema(ma.ModelSchema):
    class Meta:
        model = Stores
