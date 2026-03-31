import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

# 權限範圍：需要讀取 (readonly) 與 寫入 (force-ssl) 播放清單
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

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
