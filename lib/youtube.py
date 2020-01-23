import httplib2
import os
from glob import glob

import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

scopes = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

httplib2.debuglevel = 4


class YouTube:
    def __init__(self, storage_file='./secrets/credentials.storage'):
        self.storage_file = storage_file
        self.youtube = None

    def get_credentials(self):
        client_secrets_files = glob("./secrets/client_secret_*.json")
        client_secrets_file = client_secrets_files[0]

        storage = Storage(self.storage_file)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            flow = flow_from_clientsecrets(
                client_secrets_file, scope=scopes)
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

    def video_categories(self):
        request = self.youtube.videoCategories().list(
            part="snippet",
            regionCode="US"
        )
        return request.execute()
