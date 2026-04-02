import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Scopes: Need read (readonly) and write (force-ssl) permissions for playlists
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

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
