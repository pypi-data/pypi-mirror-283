import os
import time
import threading
import queue
from appdirs import user_cache_dir
from ytmusicapi import YTMusic
import yt_dlp
import vlc
import argparse

APP_NAME = "YTMusicPlayer"
CACHE_DIR = user_cache_dir(APP_NAME)

def ensure_cache_dir():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def get_cached_file(video_id):
    for file in os.listdir(CACHE_DIR):
        if file.startswith(f"{video_id}_"):
            return os.path.join(CACHE_DIR, file)
    return None

def search_and_download_song(query, ytmusic):
    search_results = ytmusic.search(query, filter="songs", limit=1)
    
    if not search_results:
        print("No results found.")
        return None, None
    
    video_id = search_results[0]['videoId']
    title = search_results[0]['title']
    
    cached_file = get_cached_file(video_id)
    if cached_file:
        print(f"Using cached file: {os.path.basename(cached_file)}")
        return cached_file, video_id
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(CACHE_DIR, f'{video_id}_%(title)s.%(ext)s'),
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
    mp3_filename = os.path.splitext(filename)[0] + '.mp3'
    print(f"Downloaded: {os.path.basename(mp3_filename)}")
    return mp3_filename, video_id

def get_recommendations(video_id, ytmusic):
    watch_playlist = ytmusic.get_watch_playlist(video_id)
    return watch_playlist.get('tracks', [])[1:]

def render_controls(loop_enabled):
    print("\n" + "="*50)
    print("Controls:")
    print("p: Play/Pause | n: Next Song | b: Previous Song")
    print(f"l: {'Disable' if loop_enabled else 'Enable'} Loop | q: Quit")
    print("="*50)

def prefetch_next_song(playlist, current_index, ytmusic):
    if current_index + 1 < len(playlist):
        next_song = playlist[current_index + 1]
        search_and_download_song(next_song['title'], ytmusic)

def play_audio(song_queue, command_queue, ytmusic):
    instance = vlc.Instance()
    player = instance.media_player_new()
    current_index = 0
    playlist = []
    prefetch_thread = None
    loop_enabled = False

    while True:
        if not playlist or current_index >= len(playlist):
            if song_queue.empty():
                break
            song = song_queue.get()
            playlist.append(song)

        filename, video_id = search_and_download_song(playlist[current_index]['title'], ytmusic)
        if not filename:
            current_index += 1
            continue

        media = instance.media_new(filename)
        player.set_media(media)
        player.play()
        print(f"\nNow playing: {os.path.basename(filename)}")
        render_controls(loop_enabled)

        if prefetch_thread and prefetch_thread.is_alive():
            prefetch_thread.join()

        if current_index == len(playlist) - 1:
            new_recommendations = get_recommendations(video_id, ytmusic)
            playlist.extend(new_recommendations)

        prefetch_thread = threading.Thread(target=prefetch_next_song, args=(playlist, current_index, ytmusic))
        prefetch_thread.start()

        while True:
            if player.get_state() == vlc.State.Ended:
                if loop_enabled:
                    player.set_position(0)
                    player.play()
                else:
                    current_index += 1
                    break

            try:
                cmd = command_queue.get_nowait()
                if cmd == 'p':
                    if player.is_playing():
                        player.pause()
                        print("Paused")
                    else:
                        player.play()
                        print("Resumed")
                elif cmd == 'n':
                    current_index += 1
                    break
                elif cmd == 'b':
                    if current_index > 0:
                        current_index -= 1
                        break
                    else:
                        print("No previous song available")
                elif cmd == 'l':
                    loop_enabled = not loop_enabled
                    print(f"Loop {'enabled' if loop_enabled else 'disabled'}")
                    render_controls(loop_enabled)
                elif cmd == 'q':
                    player.stop()
                    return
            except queue.Empty:
                time.sleep(0.1)

        player.stop()

    if prefetch_thread and prefetch_thread.is_alive():
        prefetch_thread.join()

def main():
    parser = argparse.ArgumentParser(description="Play music from YouTube Music")
    parser.add_argument("query", nargs="+", help="The song or artist to search for")
    args = parser.parse_args()

    ensure_cache_dir()
    ytmusic = YTMusic()
    song_queue = queue.Queue()
    command_queue = queue.Queue()

    print(f"Using cache directory: {CACHE_DIR}")
    query = " ".join(args.query)
    print(f"Searching for: {query}")
    initial_song = {'title': query}
    song_queue.put(initial_song)

    player_thread = threading.Thread(target=play_audio, args=(song_queue, command_queue, ytmusic))
    player_thread.start()

    try:
        while player_thread.is_alive():
            cmd = input().lower()
            if cmd in ['p', 'n', 'b', 'l', 'q']:
                command_queue.put(cmd)
            if cmd == 'q':
                break
    finally:
        player_thread.join()
        print("Thank you for using the YouTube Music Player!")

if __name__ == "__main__":
    main()