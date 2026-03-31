import os
from youtube_auth import get_authenticated_service

def list_my_playlists(youtube):
    print("📋 正在獲取你的所有播放清單...")
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=50
    )
    response = request.execute()

    print(f"{'Playlist Title':<30} | {'Songs':<6} | {'Playlist ID'}")
    print("-" * 70)
    
    # 手動加上 Liked Videos (因為 mine=True 不會列出它)
    print(f"{'Liked Videos (點讚紀錄)':<30} | {'?':<6} | {'LL'}")

    for item in response.get("items", []):
        title = item["snippet"]["title"]
        count = item["contentDetails"]["itemCount"]
        playlist_id = item["id"]
        print(f"{title:<30} | {count:<6} | {playlist_id}")

def main():
    youtube = get_authenticated_service()
    if youtube:
        list_my_playlists(youtube)

if __name__ == "__main__":
    main()
