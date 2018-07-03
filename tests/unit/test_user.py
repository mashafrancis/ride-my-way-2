import json

data = {
    '1': {
        "firstname": "Francis",
        "lastname": "Masha",
        "email": "masha@gmail.com",
        "password": "bhakita",
        "confirm_password": "bhakita"
    },
    '2': {
        "email": "francismasha@gmail.com",
        "password": "blablabla"
    },
    '3': {
        "firstname": "Francis",
        "lastname": "Konde",
        "email": "franciskonde@gmail.com",
        "password": "blablabla",
        "confirm_password": "blablabla"
    },
    '4': {
        "email": "franciskonde@gmail.com",
        "password": "blablabla"
    }
}


def test_create_user(test_client):
    res = test_client.post('/v1/auth/signup')
    assert res.status_code == 201


def test_edit_user(test_client):
    res = test_client.put('/v1/users/1',
                          data=json.dumps(data['3']),
                          headers={'Content-Type': 'application/json'})
    assert res.status_code == 200


def test_delete_user(test_client):
    res = test_client.delete('/v1/users/1')
    assert res.status_code == 200


def test_login_with_good_credentials(test_client):
    test_client.post('/v1/auth/signup',
                     data=json.dumps(data['1']),
                     content_type='application/json')
    res = test_client.post('v1/auth/login',
                           data=json.dumps(data['2']),
                           headers={'Content-Type': 'application/json'})
    assert res.status_code == 200


def test_login_with_bad_credentials(test_client):
    test_client.post('/v1/auth/signup',
                     data=json.dumps(data['1']),
                     headers={'Content-Type': 'application/json'})
    res = test_client.post('v1/auth/login',
                           data=json.dumps(data['4']),
                           headers={'Content-Type': 'application/json'})
    assert res.status_code == 400
