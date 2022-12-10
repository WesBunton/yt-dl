import argparse
import sys
import yt_dlp
# This script is for automating the downloading of YouTube videos from YouTube Studio.

# This is the NFS share mount for pushing downloaded videos to the NAS
download_path = {'home':'/mnt/videoshare'}

def download_video(url):
    yt_opts = {
        'verbose': True,
        'paths':download_path
    }
    ydl = yt_dlp.YoutubeDL(yt_opts)
    print("Starting download with URL: " + url)
    ydl.download(url)
    print("Download complete!")

def main():
    parser=argparse.ArgumentParser(
        description='''YouTube video downloader:''',
        epilog="""Happy downloading...""",
        usage='python3 yt.py --url video-url')
    required = parser.add_argument_group('required arguments')
    required.add_argument('--url', help='URL of YouTube video')
    args=parser.parse_args()
    if args.url is None:
        sys.exit('Need a URL...')
    url = args.url
    download_video(url)

if __name__ == "__main__":
    main()
