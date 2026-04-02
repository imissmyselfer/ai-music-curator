import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from youtube_auth import SCOPES  # Use our refactored SCOPES

def get_authenticated_service():
    """Handle OAuth2 authorization and return the API service object"""
    client_secrets_file = "client_secrets.json"
    if not os.path.exists(client_secrets_file):
        print(f"\n❌ Error: {client_secrets_file} not found")
        return None

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_local_server(port=0)
    
    return googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

def is_likely_music(item):
    """Preliminary judgment on whether it is a music video"""
    snippet = item.get("snippet", {})
    title = snippet.get("title", "").lower()
    
    # Exclude common non-song keywords
    exclude_keywords = ["vlog", "tutorial", "news", "unboxing", "review", "live stream"]
    for word in exclude_keywords:
        if word in title:
            return False
            
    # If it contains " - Topic", it's usually an official YouTube Music track, a high-quality source
    artist = snippet.get("videoOwnerChannelTitle", "")
    if " - Topic" in artist:
        return True
        
    return True

import yaml

def load_config():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def fetch_liked_songs(youtube, playlist_id, total_to_fetch=500):
    """Fetch music from a specified playlist"""
    songs = []
    next_page_token = None
    fetched_count = 0
    
    print(f"🎵 Fetching music data from playlist {playlist_id}...")
    
    while fetched_count < total_to_fetch:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        
        items = response.get("items", [])
        if not items:
            break
            
        for item in items:
            if is_likely_music(item):
                title = item["snippet"]["title"]
                artist = item["snippet"].get("videoOwnerChannelTitle", "Unknown")
                artist = artist.replace(" - Topic", "")
                
                songs.append({
                    "title": title,
                    "artist": artist,
                    "video_id": item["contentDetails"]["videoId"]
                })
        
        fetched_count += len(items)
        next_page_token = response.get("nextPageToken")
        print(f"   Fetched {fetched_count} items, currently found {len(songs)} songs...")
        
        if not next_page_token:
            break
            
    return songs

def main():
    config = load_config()
    playlist_id = config.get("source_playlist_id", "LL")  # Default to LL
    
    youtube = get_authenticated_service()
    if not youtube:
        return

    try:
        # Use the playlist ID from the configuration file
        liked_songs = fetch_liked_songs(youtube, playlist_id, 500)
        
        output_file = "data/liked_songs.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(liked_songs, f, ensure_ascii=False, indent=2)
            
        print(f"\n✅ Filtering complete! Successfully fetched {len(liked_songs)} songs from likes.")
        print(f"📂 Data updated to: {output_file}")

    except googleapiclient.errors.HttpError as e:
        print(f"❌ API error occurred: {e}")

if __name__ == "__main__":
    main()
