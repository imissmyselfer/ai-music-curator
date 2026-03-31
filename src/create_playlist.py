import json
import time
from youtube_auth import get_authenticated_service

def search_song(youtube, artist, song_name):
    """在 YouTube 上搜尋歌曲並回傳第一個 Video ID"""
    query = f"{artist} {song_name}"
    print(f"🔍 正在搜尋: {query}...")
    
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=1,
        type="video",
        videoCategoryId="10"  # Music 分類
    )
    response = request.execute()
    
    items = response.get("items", [])
    if items:
        return items[0]["id"]["videoId"]
    return None

def create_playlist(youtube, title, description="AI 推薦：深夜呢喃"):
    """建立一個新的 YouTube 播放清單"""
    print(f"✨ 正在建立播放清單: {title}...")
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "defaultLanguage": "zh-TW"
            },
            "status": {
                "privacyStatus": "private"  # 預設為私有，你可以手動公開
            }
        }
    )
    response = request.execute()
    return response["id"]

def add_song_to_playlist(youtube, playlist_id, video_id):
    """將影片加入播放清單"""
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
    # 1. 載入 AI 推薦資料
    with open("data/recommendations.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    playlist_title = data.get("playlist_title", "AI 推薦歌單")
    recommendations = data.get("recommendations", [])

    if not recommendations:
        print("❌ 錯誤: 找不到推薦歌曲。請先執行 src/main.py")
        return

    # 2. 認證 YouTube API
    youtube = get_authenticated_service()
    if not youtube:
        return

    # 3. 建立播放清單
    try:
        playlist_id = create_playlist(youtube, playlist_title)
        print(f"✅ 播放清單已建立，ID: {playlist_id}")

        # 4. 搜尋並加入歌曲
        for rec in recommendations:
            video_id = search_song(youtube, rec["artist"], rec["song_name"])
            if video_id:
                add_song_to_playlist(youtube, playlist_id, video_id)
                print(f"   🎵 已加入: {rec['song_name']} - {rec['artist']}")
                # 稍微延遲避免觸發 API 頻率限制
                time.sleep(1)
            else:
                print(f"   ⚠️ 找不到歌曲: {rec['song_name']} - {rec['artist']}")

        print(f"\n🎉 全部完成！你的 AI 專屬歌單『{playlist_title}』已經在 YouTube Music 上準備好了！")

    except Exception as e:
        print(f"❌ 執行過程中發生錯誤: {e}")

if __name__ == "__main__":
    main()
