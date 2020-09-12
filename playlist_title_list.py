import os
import sys
import time
import googleapiclient
import googleapiclient.discovery
import googleapiclient.errors


if "YOUTUBE_API_KEY" not in os.environ:
    print("YOUTUBE_API_KEY not provided")
    sys.exit(0)

# Build playlist set save to file
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=os.getenv("YOUTUBE_API_KEY"))


BASE_EMBED_URL = "http://www.youtube.com/embed/videoseries?list="
page_token = ""
hasNextPage = True
f = open("channel_playlists_url.txt", "a")
counter = 0
while hasNextPage:
    time.sleep(3)
    request = youtube.playlists().list(
        part="id,localizations,player,snippet",
        channelId="UCTsFhKAF7i0KklHZ8NGqOoQ",
        maxResults=50,
        pageToken=page_token
    )
    playlist = request.execute()
    try:
        page_token = playlist["nextPageToken"]
    except KeyError:
        print("Ran out of pages. Stopping.")
        hasNextPage = False
    for item in playlist["items"]:
        title = item["snippet"]["title"]
        embed_url = BASE_EMBED_URL + item["id"]
        print("%s - %s" % (counter, title))
        f.write(title + " - " + embed_url + "\n")
        counter += 1

f.close()
