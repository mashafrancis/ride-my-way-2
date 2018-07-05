def test_user_request_ride(test_client):
    """
    This tests whether the user can successfully request a ride
    :param test_client:
    :return:201
    """
    response = test_client.post('/v1/rides/<ride_id>/requests',
                                headers={'Content-Type': 'application/json'})
    assert response.status_code == 201


def test_user_get_one(test_client):
    """
    Tests user successfully getting a ride request
    :param test_client:
    :return: 200
    """
    response = test_client.post('/v1/rides/<ride_id>/requests',
                                headers={'Content-Type': 'application/json'})
    assert response.status_code == 200


def test_get_ride_requests(test_client):
    response = test_client.post('/v1/rides/requests',
                                headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

