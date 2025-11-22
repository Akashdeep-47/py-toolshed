import os
import re
import subprocess
from yt_dlp import YoutubeDL

def download_playlist_with_ytdlp(playlist_url, output_folder):
    """
    Downloads all videos from a YouTube playlist using the absolute highest 
    quality video and audio streams available, then merges them.
    
    Requires:
    1. The 'yt-dlp' Python library.
    2. The 'ffmpeg' command-line tool for stream merging.
    """
    
    # 1. Sanitize the output folder name and create it
    # Note: Added 'utf-8' encoding to handle complex characters in folder names.
    safe_folder_name = re.sub(r'[\\/:*?"<>|]', '', output_folder).encode('utf-8', 'ignore').decode('utf-8')
    
    if not os.path.exists(safe_folder_name):
        os.makedirs(safe_folder_name)
        print(f"✅ Created output directory: {safe_folder_name}")
    else:
        print(f"✅ Output directory already exists: {safe_folder_name}")

    # 2. yt-dlp Options
    ydl_opts = {
        # General file name structure: 
        'outtmpl': os.path.join(safe_folder_name, '%(playlist_index)s - %(title)s.%(ext)s'),
        
        # ⬇️ CRITICAL CHANGE FOR HIGHEST QUALITY ⬇️
        # 'bestvideo+bestaudio' ensures the highest resolution video stream 
        # and the highest bitrate audio stream are downloaded separately and merged.
        # The '/best' fallback is for older videos that might not have separate streams.
        # This requires FFmpeg for merging.
        'format': 'bestvideo+bestaudio/best', 
        
        # Ensures the merged file is put into an MP4 container for maximum compatibility.
        'merge_output_format': 'mp4',
        
        # Behavior settings
        'ignoreerrors': True, # Skip videos that fail instead of crashing
        'progress_hooks': [lambda d: print(f"   Downloading: {d['filename']}" if d['status'] == 'downloading' else "")],
        'cachedir': False, # Don't use a cache that might hold broken info
        'noplaylist': False, # Ensure we process the whole playlist
        'noprogress': True, # Keep output clean
    }

    print(f"\n🌟 Starting download for playlist (Highest Quality): {playlist_url}")
    print(f"   Files will be saved to: {safe_folder_name}")
    print("   ⚠️ **FFmpeg is required for merging the highest quality video and audio streams.**")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # ydl.extract_info handles the entire playlist download and merging
            ydl.download([playlist_url])
            
        print("\n\n🎉 **Playlist video download (Highest Quality) complete!**")
        
    except Exception as e:
        print(f"\n❌ A critical error occurred during yt-dlp execution.")
        print(f"   Ensure FFmpeg is installed and accessible via PATH for file merging.")
        print(f"   Detailed Error: {e}")


if __name__ == "__main__":
    # --- User Input ---
    playlist_link = input("Enter the YouTube Playlist URL: ")
    folder_name = input("Enter the folder name to save the videos: ")
    # ------------------
    
    download_playlist_with_ytdlp(playlist_link, folder_name)