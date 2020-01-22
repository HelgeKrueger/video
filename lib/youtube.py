import httplib2
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

scopes = ["https://www.googleapis.com/auth/youtube.upload"]


class YouTube:
    def __init__(self, storage_file='./secrets/credentials.storage'):
        self.storage_file = storage_file
        self.youtube = None

    def get_credentials(self):
        client_secrets_file = "./secrets/client_secret_740234423024-occj070rtcrheme1fpvlr9a3avsoeoq5.apps.googleusercontent.com.json"

        storage = Storage(self.storage_file)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            flow = flow_from_clientsecrets(
                client_secrets_file, scope=scopes[0])
            credentials = run_flow(flow, storage, http=httplib2.Http())

        self.credentials = credentials

    def init(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        self.get_credentials()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=self.credentials)

    def upload_file(self, filename, title, description):
        upload_body = {
            "snippet": {
                "categoryId": "22",
                "description": description,
                "title": title,
            },
            "status": {
                "privacyStatus": "public"
            }
        }
        media = MediaFileUpload(filename, resumable=True)

        try:
            request = self.youtube.videos().insert(
                part="snippet,status",
                body=upload_body,
                media_body=media
            )
            response = None
            # response = request.execute()
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print("Uploaded %d%%." % int(status.progress() * 100))
            print("Upload Complete!")
            print(response)
        except googleapiclient.errors.HttpError as err:
            print(err)
            print(err.content)
            print(err.error_details)
