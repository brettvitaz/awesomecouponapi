from datetime import datetime
from flask_marshmallow import Marshmallow

from api.models import Coupons, Stores

ma = Marshmallow()


class CouponDateTime(ma.Field):
    """A formatted Coupon DateTime.
    
    Ensures proper (de)serialization of Coupon DateTime values.
    
    e.g. ``'2016-08-05T08:40:51.620Z'``
    """

    default_error_messages = {
        'invalid': 'Not a valid datetime.',
        'format': '"{input}" does not match format {format}.',
    }

    format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def _deserialize(self, value, attr, obj):
        if value is None:
            return None
        try:
            return datetime.strptime(value, self.format)
        except ValueError:
            self.fail('format', input=value, format=self.format)

    def _serialize(self, value, attr, data):
        if not value:  # Falsy values, e.g. '', None, [] are not valid
            raise self.fail('invalid')

        try:
            return f"{value.isoformat(timespec='milliseconds')}Z"
        except AttributeError:
            self.fail('invalid')


class CouponsSchema(ma.ModelSchema):
    expire_at = CouponDateTime()
    published_at = CouponDateTime()
    store = ma.Nested('StoresSchema', exclude=('id',))

    class Meta:
        model = Coupons


class StoresSchema(ma.ModelSchema):
    class Meta:
        model = Stores
