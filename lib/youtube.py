# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.insert
# NOTES:
# 1. This sample code uploads a file and can't be executed via this interface.
#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/guides/code_samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

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


def get_credentials():
    client_secrets_file = "./secrets/client_secret_740234423024-m2hdv91nbse10mfldt162njrd9matut0.apps.googleusercontent.com.json"

    storage = Storage('./secrets/credentials.storage')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(client_secrets_file, scope=scopes[0])
        credentials = run_flow(flow, storage, http=httplib2.Http())

    return credentials


def upload_file(youtube, filename, title, description):
    upload_body = {
        "snippet": {
            "categoryId": "22",
            "description": "Description of uploaded video.",
            "title": "More empty road"
        },
        "status": {
            "privacyStatus": "public"
        }
    }
    media = MediaFileUpload(filename, resumable=True)

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=upload_body
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


def create_youtube():
    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    credentials = get_credentials()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return youtube


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = create_youtube()
    upload_file(youtube, "emptyroad2.mp4", "empty road", "blablabla")


if __name__ == "__main__":
    main()
