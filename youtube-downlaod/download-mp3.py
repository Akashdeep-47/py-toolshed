import os
import re
import subprocess
from yt_dlp import YoutubeDL

def download_playlist_with_ytdlp(playlist_url, output_folder):
    """
    Downloads all videos from a YouTube playlist and converts them to MP3 using yt-dlp.
    
    Requires:
    1. The 'yt-dlp' Python library.
    2. The 'ffmpeg' command-line tool (yt-dlp uses this internally for conversion).
    """
    
    # 1. Sanitize the output folder name and create it
    safe_folder_name = re.sub(r'[\\/:*?"<>|]', '', output_folder)
    
    if not os.path.exists(safe_folder_name):
        os.makedirs(safe_folder_name)
        print(f"✅ Created output directory: {safe_folder_name}")
    else:
        print(f"✅ Output directory already exists: {safe_folder_name}")

    # 2. yt-dlp Options
    ydl_opts = {
        # General file name structure: 
        # %(playlist_index)s ensures correct playlist order
        'outtmpl': os.path.join(safe_folder_name, '%(playlist_index)s - %(title)s.%(ext)s'),
        
        # Audio conversion settings
        'format': 'bestaudio/best',  # Selects the best audio format
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # High quality MP3
        }],
        
        # Behavior settings
        'ignoreerrors': True, # Skip videos that fail instead of crashing
        'progress_hooks': [lambda d: print(f"   Downloading: {d['filename']}" if d['status'] == 'downloading' else "")],
        'cachedir': False, # Don't use a cache that might hold broken info
        'noplaylist': False, # Ensure we process the whole playlist
        'noprogress': True, # Keep output clean
    }

    print(f"\n🎧 Starting download and conversion for playlist: {playlist_url}")
    print(f"   Files will be saved to: {safe_folder_name}")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # ydl.extract_info handles the entire playlist download and conversion
            ydl.download([playlist_url])
            
        print("\n\n🎉 **Playlist download and conversion complete!**")
        
    except Exception as e:
        print(f"\n❌ A critical error occurred during yt-dlp execution.")
        print(f"   Ensure FFmpeg is installed and accessible via PATH.")
        print(f"   Detailed Error: {e}")


if __name__ == "__main__":
    # --- User Input ---
    playlist_link = input("Enter the YouTube Playlist URL: ")
    folder_name = input("Enter the folder name to save the MP3s: ")
    # ------------------
    
    download_playlist_with_ytdlp(playlist_link, folder_name)