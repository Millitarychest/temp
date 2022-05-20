from TikTokAPI import TikTokAPI
import os
import random
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import datetime
from googleapiclient.http import MediaFileUpload
import time



scopes = ["https://www.googleapis.com/auth/youtube.upload"]

client_secrets_file = "client_secret_936408558953-31la4aoagm1klb3aieu0cklhp4v6qjcg.apps.googleusercontent.com.json"
upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'
# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()

def main():

    ## Tik Tok
    api = TikTokAPI()
    response = api.getVideosByHashTag("#badassanimemoments", count=30)
    tiktok = random.randint(0, 29)
    print(tiktok)
    api.downloadVideoById(response["itemList"][tiktok]["id"], "./out/" + response["itemList"][tiktok]["id"] + ".mp4")

    path = "./out/" + response["itemList"][tiktok]["id"] + ".mp4"
    ## youtube
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        notifySubscribers=True,
        body = {
            'snippet': {
                'categoryI': 19,
                'title': 'Upload Testing',
                'description': 'Hello World Description',
                'tags': ['Travel', 'video test', 'Travel Tips']
            },
            'status': {
                'privacyStatus': 'private',
                'publishAt': upload_date_time,
                'selfDeclaredMadeForKids': False, 
            },
            'notifySubscribers': False
        },

            
        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload(path)
    )
    request.execute()

while(1):
    main()
    time.sleep(86400)