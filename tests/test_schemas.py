from datetime import datetime
from marshmallow import ValidationError
import pytest

from api import schemas


class TestCouponDateTime:
    def setup(self):
        self.field = schemas.CouponDateTime()

    def test_deserialize(self):
        expected = datetime(2016, 8, 5, 8, 40, 51, 620000)

        value = '2016-08-05T08:40:51.620Z'
        result = self.field.deserialize(value)
        assert result == expected

    def test_deserialize_fail(self):
        value = '--08-05T08:40:51.620Z'
        with pytest.raises(ValidationError) as e:
            result = self.field.deserialize(value)
        assert 'does not match format' in str(e.value)

    def test_deserialize_fail_none(self):
        value = None
        with pytest.raises(ValidationError) as e:
            result = self.field.deserialize(value)
        assert 'Field may not be null.' in str(e.value)

    def test_serialize(self):
        expected = '2016-08-05T08:40:51.620Z'

        obj = {
            'value': datetime(2016, 8, 5, 8, 40, 51, 620000)
        }
        result = self.field.serialize('value', obj)
        assert result == expected

    def test_serialize_fail_none(self):
        obj = {
            'value': None
        }
        with pytest.raises(ValidationError) as e:
            result = self.field.serialize('value', obj)
        assert 'Not a valid datetime.' in str(e.value)

    def test_serialize_fail_attr_err(self):
        obj = {
            'value': object
        }
        with pytest.raises(ValidationError) as e:
            result = self.field.serialize('value', obj)
        assert 'Not a valid datetime.' in str(e.value)
