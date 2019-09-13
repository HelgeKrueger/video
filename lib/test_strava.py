from .strava import Strava


def test_strava_retrieves_an_activity():
    s = Strava()

    assert type(s.retrieve_last_activity_id()) == int
