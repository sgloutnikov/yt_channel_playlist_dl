import youtube_dl
import os
import sys
import time
import googleapiclient
import googleapiclient.discovery
import googleapiclient.errors


CHANNEL_ID = "UCTsFhKAF7i0KklHZ8NGqOoQ"
START_PAGE = 0
# Exclusive page number
END_PAGE = 10
PAGE_SIZE = 10
BASE_EMBED_URL = "http://www.youtube.com/embed/videoseries?list="


if "YOUTUBE_API_KEY" not in os.environ:
    print("YOUTUBE_API_KEY not provided")
    sys.exit(0)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256',
    }],
    'outtmpl': 'download/%(playlist_title)s/%(title)s.%(etx)s',
    'quiet': False
}


def get_youtube_playlist(channel_id, max_result=10, page_token=""):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=os.getenv("YOUTUBE_API_KEY"))
    request = youtube.playlists().list(
        part="id,localizations,player,snippet",
        channelId=channel_id,
        maxResults=max_result,
        pageToken=page_token
    )
    response = request.execute()
    return response


def download_playlist(playlist_url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


if __name__ == '__main__':
    current_page = 0
    next_page_token = ""
    hasNextPage = True
    while current_page < END_PAGE and hasNextPage:
        time.sleep(2)
        # Always start from first page, skip until reached START_PAGE
        playlist = get_youtube_playlist(channel_id=CHANNEL_ID, max_result=PAGE_SIZE,
                                        page_token=next_page_token)
        try:
            next_page_token = playlist["nextPageToken"]
        except KeyError:
            print("Ran out of pages. Stopping.")
            hasNextPage = False
        if current_page >= START_PAGE:
            print("Downloading Page %s Token: %s" % (current_page, next_page_token))
            for item in playlist["items"]:
                embed_url = BASE_EMBED_URL + item["id"]
                print("++ Download Full URL: %s" % embed_url)
                download_playlist(embed_url)
        else:
            print("Skipping Page %s" % current_page)
        current_page += 1
