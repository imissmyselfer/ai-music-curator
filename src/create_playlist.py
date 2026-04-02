import json
import time
from youtube_auth import get_authenticated_service

def search_song(youtube, artist, song_name):
    """Search for a song on YouTube and return the first Video ID"""
    query = f"{artist} {song_name}"
    print(f"🔍 Searching: {query}...")
    
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=1,
        type="video",
        videoCategoryId="10"  # Music category
    )
    response = request.execute()
    
    items = response.get("items", [])
    if items:
        return items[0]["id"]["videoId"]
    return None

def create_playlist(youtube, title, description="AI Recommendation: Midnight Whispers"):
    """Create a new YouTube playlist"""
    print(f"✨ Creating playlist: {title}...")
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "private"  # Default to private, you can manually make it public
            }
        }
    )
    response = request.execute()
    return response["id"]

def add_song_to_playlist(youtube, playlist_id, video_id):
    """Add a video to the playlist"""
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    return request.execute()

def main():
    # 1. Load AI recommendation data
    with open("data/recommendations.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    playlist_title = data.get("playlist_title", "AI Recommended Playlist")
    recommendations = data.get("recommendations", [])

    if not recommendations:
        print("❌ Error: No recommended songs found. Please run src/main.py first.")
        return

    # 2. Authenticate YouTube API
    youtube = get_authenticated_service()
    if not youtube:
        return

    # 3. Create playlist
    try:
        playlist_id = create_playlist(youtube, playlist_title)
        print(f"✅ Playlist created, ID: {playlist_id}")

        # 4. Search and add songs
        for rec in recommendations:
            video_id = search_song(youtube, rec["artist"], rec["song_name"])
            if video_id:
                add_song_to_playlist(youtube, playlist_id, video_id)
                print(f"   🎵 Added: {rec['song_name']} - {rec['artist']}")
                # Slight delay to avoid triggering API rate limits
                time.sleep(1)
            else:
                print(f"   ⚠️ Song not found: {rec['song_name']} - {rec['artist']}")

        print(f"\n🎉 All done! Your AI exclusive playlist '{playlist_title}' is ready on YouTube Music!")

    except Exception as e:
        print(f"❌ Error occurred during execution: {e}")

if __name__ == "__main__":
    main()
