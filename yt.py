import argparse
import sys
import yt_dlp
from youtube_api import YouTubeDataAPI
from datetime import datetime, timedelta

# This script is for automating the downloading of YouTube videos from YouTube Studio.

# This is the NFS share mount for pushing downloaded videos to the NAS
download_path = {'home':'/mnt/videoshare'}
yt_url_prefix = 'https://youtu.be/'

def download_video(url):
    yt_opts = {
        'verbose': True,
        'paths':download_path
    }
    ydl = yt_dlp.YoutubeDL(yt_opts)
    print("Starting download with URL: " + url)
    ydl.download(url)
    print("Download complete!")

def download_recent_livestreams(apikey, channelid):
    print('Talking to YouTube via Data API...')
    yt = YouTubeDataAPI(apikey)
    if yt.verify_key:
        print('Key is valid!')
    else:
        print('Key is not valid?!')

    # Need to generate dateime from last few weeks
    weeks_ago_datetime = datetime.today() - timedelta(days=14)
    print('Calculating datetime to search for videos from last few weeks...')
    print(weeks_ago_datetime)

    print('Searching for videos...')
    search_res_ls = yt.search(
        'a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z',  # empty search value returns None
        channel_id=channelid,
        published_after=weeks_ago_datetime,
        order_by='date',
        event_type='completed',
        type='video',
        video_duration='any',
        max_results=10
        )
    if len(search_res_ls) == 0:
        print('No results returns?!')
    
    for search_res in search_res_ls:
        print(str(search_res))
        new_url = yt_url_prefix + search_res['video_id']
        print('Attempting to download via generated URL: ' + new_url)
        download_video(new_url)
        print('\n')

def main():
    parser=argparse.ArgumentParser(
        description='''YouTube video downloader:''',
        epilog="""Happy downloading...""",
        usage='python3 yt.py --url to download a single video or with no params to download recent livestreams')
    required = parser.add_argument_group('required arguments')
    required.add_argument('--url', help='URL of YT video')
    required.add_argument('--apikey', help='YT Data Api Key')
    required.add_argument('--channelid', help='YT Channel ID')
    args=parser.parse_args()

    if args.url is None:
        if args.apikey is None:
            sys.exit('No URL or API Key given...')
        else:
            apikey = args.apikey

        if args.channelid is None:
            sys.exit('No URL or Channel ID given...')
        else:
            channelid = args.channelid

        print('No URL provided, searching for recent livestreams instead...')
        download_recent_livestreams(apikey=apikey, channelid=channelid)
    else:
        url = args.url
        download_video(url)

if __name__ == "__main__":
    main()
