import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# 設定 API 權限範圍：唯讀播放清單與喜歡的內容
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_authenticated_service():
    """處理 OAuth2 授權並回傳 API 服務物件"""
    client_secrets_file = "client_secrets.json"
    
    if not os.path.exists(client_secrets_file):
        print(f"\n❌ 錯誤: 找不到 {client_secrets_file}")
        print("請到 Google Cloud Console 下載 OAuth 2.0 用戶端 ID 的 JSON 檔案並重新命名為 client_secrets.json")
        return None

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_local_server(port=0)
    
    return googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

def fetch_liked_songs(youtube, max_results=100):
    """抓取喜歡的歌曲清單"""
    songs = []
    next_page_token = None
    
    print(f"🎵 開始抓取前 {max_results} 首喜歡的歌曲...")
    
    while len(songs) < max_results:
        # LL 是 YouTube 中 'Liked Videos' 的特殊 Playlist ID
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId="LL",
            maxResults=min(50, max_results - len(songs)),
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            artist = item["snippet"].get("videoOwnerChannelTitle", "Unknown")
            # 移除常見的 YouTube 尾綴
            artist = artist.replace(" - Topic", "")
            
            songs.append({
                "title": title,
                "artist": artist,
                "video_id": item["contentDetails"]["videoId"]
            })
            
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
            
    return songs

def main():
    youtube = get_authenticated_service()
    if not youtube:
        return

    try:
        liked_songs = fetch_liked_songs(youtube, 100)
        
        # 將結果存入 data/liked_songs.json
        output_file = "data/liked_songs.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(liked_songs, f, ensure_ascii=False, indent=2)
            
        print(f"\n✅ 成功抓取 {len(liked_songs)} 首歌！")
        print(f"📂 資料已存至: {output_file}")
        
        # 印出前 5 首看看
        print("\n📻 最近喜歡的 5 首歌:")
        for i, song in enumerate(liked_songs[:5], 1):
            print(f"{i}. {song['title']} - {song['artist']}")

    except googleapiclient.errors.HttpError as e:
        print(f"❌ 發生 API 錯誤: {e}")

if __name__ == "__main__":
    main()
