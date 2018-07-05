from app.models.ride import RideModel


def test_create_ride():
    ride = RideModel(1, 'Buruburu', 'Thika', '10 May 2018', '9:00')
    assert ride.ride_id == 1
    assert ride.origin == 'Buruburu'
    assert ride.destination == 'Thika'
    assert ride.date == '10 May 2018'
    assert ride.time == '9:00'


def test_item_json():
    ride = RideModel(1, 'Buruburu', 'Thika', '10 May 2018', '9:00')
    expected = {
        'ride_id': 1,
        'origin': 'Buruburu',
        'destination': 'Thika',
        'date': '10 May 2018',
        'time': '9:00'
    }

    assert ride.json() == expected



