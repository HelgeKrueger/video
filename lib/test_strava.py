import pytest
import os

from .strava import Strava

@pytest.mark.skipif(not os.path.exists('../secrets/strava.yml'), reason="Needs a strava account")
def test_strava_retrieves_an_activity():
    s = Strava()

    assert type(s.retrieve_last_activity_id()) == int
