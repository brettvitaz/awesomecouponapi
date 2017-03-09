import pytest
import simplejson as json

from api import app


@pytest.fixture
def client(tmpdir):
    def fn(init_db=True, do_import=True):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{tmpdir.strpath}/coupon-db.sqlite'
        app.app.config['TESTING'] = True
        app.init_app(app.app)
        test_client = app.app.test_client()

        if init_db:
            with app.app.app_context():
                app.init_db(do_import)

        return test_client

    return fn


@pytest.fixture
def coupons():
    with open('./coupons.json') as f:
        return json.load(f)


def test_route_coupons(client, coupons):
    rv = client().get('/coupons')
    assert rv.status_code == 200

    all_coupons = json.loads(rv.data)
    assert len(all_coupons) == 20

    for i, coupon in enumerate(all_coupons):
        coupons[i].update(id=i + 1)
        assert json.dumps(coupon, sort_keys=True) == json.dumps(coupons[i], sort_keys=True)


def test_route_coupons_invalid(client):
    rv = client().get('/coupons?status=invalid')
    assert rv.status_code == 200

    coupons = json.loads(rv.data)
    assert len(coupons) == 3


def test_route_coupons_valid(client):
    rv = client().get('/coupons?status=valid')
    assert rv.status_code == 200

    coupons = json.loads(rv.data)
    assert len(coupons) == 17


def test_route_coupons_bad_filter(client):
    rv = client().get('/coupons?foo=valid')
    assert rv.status_code == 400


def test_route_coupons_empty(client):
    rv = client(do_import=False).get('/coupons')
    assert rv.status_code == 200

    coupons = json.loads(rv.data)
    assert len(coupons) == 0


def test_route_coupons_server_error(client):
    rv = client(init_db=False, do_import=False).get('/coupons')
    assert rv.status_code == 500

    assert b'no such table: coupons' in rv.data


def test_route_coupons_by_id_get_valid(client, coupons):
    expected = coupons[0]
    expected.update(id=1)

    rv = client().get('/coupons/1')
    assert rv.status_code == 200

    coupon = json.loads(rv.data)
    assert json.dumps(coupon, sort_keys=True) == json.dumps(expected, sort_keys=True)


def test_route_coupons_by_id_get_non_exist(client):
    rv = client().get('/coupons/21')
    assert rv.status_code == 404


def test_route_coupons_by_id_get_bad_number(client):
    rv = client().get('/coupons/-1')
    assert rv.status_code == 400


def test_route_coupons_by_id_get_bad_other(client):
    rv = client().get('/coupons/abc')
    assert rv.status_code == 400


def test_route_coupons_by_id_put_valid(client, coupons):
    data = '{"couponcode": "UPDATED_COUPON"}'

    expected = coupons[0]
    expected.update(id=1, couponcode='UPDATED_COUPON')

    rv = client().put('/coupons/1', data=data, content_type='application/json')
    assert rv.status_code == 200

    coupon = json.loads(rv.data)
    assert json.dumps(coupon, sort_keys=True) == json.dumps(expected, sort_keys=True)


def test_route_coupons_by_id_put_invalid(client, coupons):
    data = '{"couponcode": "UPDATED_COUPON", "published_at":""}'

    expected = coupons[0]
    expected.update(id=1, couponcode='UPDATED_COUPON')

    rv = client().put('/coupons/1', data=data, content_type='application/json')
    assert rv.status_code == 400


def test_route_coupons_by_id_put_non_exist(client):
    data = '{"couponcode": "UPDATED_COUPON", "published_at":""}'

    rv = client().put('/coupons/100', data=data, content_type='application/json')
    assert rv.status_code == 404


def test_route_coupons_by_id_put_integrity_error(client):
    data = '{"couponcode": "UPDATED_COUPON", "id":"2"}'

    rv = client().put('/coupons/1', data=data, content_type='application/json')
    assert rv.status_code == 500


def test_route_coupons_by_id_put_bad_id(client):
    data = '{"couponcode": "UPDATED_COUPON"}'

    rv = client().put('/coupons/abc', data=data, content_type='application/json')
    assert rv.status_code == 400


def test_route_coupons_by_id_put_invalid_content_type(client):
    data = '{"couponcode": "UPDATED_COUPON"}'

    rv = client().put('/coupons/1', data=data, content_type='text/plain')
    assert rv.status_code == 415


def test_route_coupons_by_id_delete_valid(client):
    test_client = client()
    rv = test_client.delete('/coupons/1')
    assert rv.status_code == 204

    rv = test_client.get('/coupons')
    coupons = json.loads(rv.data)
    assert len(coupons) == 19


def test_route_coupons_by_id_delete_non_exist(client):
    test_client = client()
    rv = test_client.delete('/coupons/21')
    assert rv.status_code == 404


def test_route_add_coupon(client):
    data = '{"category":"Coupons & Special Offers","couponcode":"60 31261","description":"Offer limited to in-store purchase only.","merchant":"Super Sporting Goods","title":"20% Off 2 Regular-Priced Items and/or 10% Off 2 Sale-Priced Items","store":{"lat":47.66001,"long":-122.31313,"city":"Seattle","phone":"547-2445","state":"Wa","street":"4315 UNIVERSITY WAY N.E.","zip":"98105"},"expire_at":"2016-08-05T08:40:51.620Z","published_at":"2016-03-05T08:40:51.620Z"}'

    rv = client().post('/coupons', data=data, content_type='application/json')
    assert rv.status_code == 201

    assert rv.headers['Location'] == 'http://localhost/coupons/21'


def test_route_add_coupon_invalid_data(client):
    data = '{"category":"Coupons & Special Offers","couponcode":"60 31261","description":"Offer limited to in-store purchase only.","merchant":"Super Sporting Goods","title":"20% Off 2 Regular-Priced Items and/or 10% Off 2 Sale-Priced Items","store":{"lat":47.66001,"long":-122.31313,"city":"Seattle","phone":"547-2445","state":"Wa","street":"4315 UNIVERSITY WAY N.E.","zip":"98105"},"expire_at":"2016-08-05T08:40:51.620Z","published_at":""}'

    rv = client().post('/coupons', data=data, content_type='application/json')
    assert rv.status_code == 400

    assert b'does not match format' in rv.data


def test_route_add_coupon_invalid_content_type(client):
    data = '{"category":"Coupons & Special Offers","couponcode":"60 31261","description":"Offer limited to in-store purchase only.","merchant":"Super Sporting Goods","title":"20% Off 2 Regular-Priced Items and/or 10% Off 2 Sale-Priced Items","store":{"lat":47.66001,"long":-122.31313,"city":"Seattle","phone":"547-2445","state":"Wa","street":"4315 UNIVERSITY WAY N.E.","zip":"98105"},"expire_at":"2016-08-05T08:40:51.620Z","published_at":""}'

    rv = client().post('/coupons', data=data, content_type='text/plain')
    assert rv.status_code == 415

    assert b'Expected Content-Type: \'application/json\'' in rv.data
