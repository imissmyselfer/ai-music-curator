import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from youtube_auth import SCOPES  # 使用我們重構後的 SCOPES

def get_authenticated_service():
    """處理 OAuth2 授權並回傳 API 服務物件"""
    client_secrets_file = "client_secrets.json"
    if not os.path.exists(client_secrets_file):
        print(f"\n❌ 錯誤: 找不到 {client_secrets_file}")
        return None

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_local_server(port=0)
    
    return googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

def is_likely_music(item):
    """初步判斷是否為音樂影片"""
    snippet = item.get("snippet", {})
    title = snippet.get("title", "").lower()
    
    # 排除常見的非歌曲關鍵字
    exclude_keywords = ["vlog", "tutorial", "news", "新聞", "教學", "unboxing", "review", "直播"]
    for word in exclude_keywords:
        if word in title:
            return False
            
    # 如果有 " - Topic" 通常是 YouTube Music 的官方上架歌曲，這是高品質來源
    artist = snippet.get("videoOwnerChannelTitle", "")
    if " - Topic" in artist:
        return True
        
    return True

import yaml

def load_config():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def fetch_liked_songs(youtube, playlist_id, total_to_fetch=500):
    """從指定的播放清單中抓取音樂"""
    songs = []
    next_page_token = None
    fetched_count = 0
    
    print(f"🎵 正在從播放清單 {playlist_id} 中撈取音樂資料...")
    
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
        print(f"   已獲取 {fetched_count} 個項目，目前找到 {len(songs)} 首音樂...")
        
        if not next_page_token:
            break
            
    return songs

def main():
    config = load_config()
    playlist_id = config.get("source_playlist_id", "LL")  # 預設為 LL
    
    youtube = get_authenticated_service()
    if not youtube:
        return

    try:
        # 使用設定檔中的清單 ID
        liked_songs = fetch_liked_songs(youtube, playlist_id, 500)
        
        output_file = "data/liked_songs.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(liked_songs, f, ensure_ascii=False, indent=2)
            
        print(f"\n✅ 過濾完成！成功從點讚紀錄中撈出 {len(liked_songs)} 首音樂。")
        print(f"📂 資料已更新至: {output_file}")

    except googleapiclient.errors.HttpError as e:
        print(f"❌ 發生 API 錯誤: {e}")

if __name__ == "__main__":
    main()
