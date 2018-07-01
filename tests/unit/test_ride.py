"""
Test functionality of all endpoints on all the methods involved with rides
"""
import json

data = {
    '1': {
        'username': 'mashafrancis',
        'name': 'Francis Masha',
        'origin': 'Buruburu',
        'destination': 'CBD',
        'date': 'Mon 25 Jun 2018',
        'time': '10:00:00'
    },
    '2': {
        'username': 'moonpie',
        'name': 'Sheldon Cooper',
        'origin': 'Jericho',
        'destination': 'Kiambu',
        'date': 'Tue 26 Jun 2018',
        'time': '1:00:00'
    }
}


def test_get_rides(test_client):
    """
    Test a GET Api
    """
    response = test_client.get('/v1/rides/')
    assert response.status_code == 200


def test_get_single_ride(test_client):
    """
    Test GET Api for a single ride
    """
    res = test_client.get('/v1/rides/')
    assert res.status_code == 200


def test_get_ride_unavailable(test_client):
    """
    Test GET Api for ride not available
    """
    response = test_client.get('/v1/rides/4')
    assert response.status_code == 404


def test_create_ride(test_client):
    """
    Test a POST Api
    """
    response = test_client.post('/v1/rides/rideId',
                                data=json.dumps(data['1']),
                                headers={'Content-Type': 'application/json'})
    assert response.status_code == 201


def test_update_ride(test_client):
    """
    Test a PUT Api
    """
    response = test_client.put('/v1/rides/1',
                               data=json.dumps(data['1']),
                               headers={'Content-Type': 'application/json'})
    assert response.status_code == 200


def test_delete_ride(test_client):
    """
    Test a DELETE Api
    :return:
    """
    response = test_client.delete('/v1/rides/rideId')
    assert response.status_code == 200
