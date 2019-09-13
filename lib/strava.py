import yaml
import requests


class Strava:
    def __init__(self, secret_file='./secrets/strava.yml'):
        self.secret_file = secret_file

        self.refresh_token_url = 'https://www.strava.com/oauth/token'
        self.activity_url = 'https://www.strava.com/api/v3/athlete/activities?per_page=1'

        self._load_secrets()
        self._refresh_token()
        self._save_secrets()

    def _load_secrets(self):
        with open(self.secret_file) as f:
            self.secrets = yaml.load(f, Loader=yaml.FullLoader)

    def _save_secrets(self):
        with open(self.secret_file, 'w') as f:
            yaml.dump(self.secrets, f)

    def _refresh_token(self):
        result = requests.post(self.refresh_token_url, {
            'client_id': self.secrets['strava_client_id'],
            'client_secret': self.secrets['strava_client_secret'],
            'grant_type': 'refresh_token',
            'refresh_token': self.secrets['strava_user_refresh_token']})

        result_dict = result.json()

        self.secrets['strava_user_refresh_token'] = result_dict['refresh_token']
        self.access_token = result_dict['access_token']

    def retrieve_last_activity_id(self):
        result = requests.get(self.activity_url, headers={
            'Authorization': 'Bearer {}'.format(self.access_token)
        })

        return result.json()[0]['id']
