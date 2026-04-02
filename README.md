# 🎵 AI-Music-Curator (AI Mandarin Music Curator)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AI Model](https://img.shields.io/badge/AI_Model-Gemini_2.5_Pro-purple.svg)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **"From the ethereal voice of Faye Wong to the resilient spirit of Stefanie Sun, let AI understand your musical soul."**

AI-Music-Curator is an intelligent MandoPop recommendation tool powered by AI. It analyzes your "Liked Songs" from YouTube Music and leverages Google Gemini 2.5 Pro's deep semantic understanding to discover kindred musical spirits and automatically generate curated playlists in your account.

---

## ✨ Core Highlights

- 🎧 **Deep Taste Analysis**: Beyond simple tags, AI analyzes the artist's essence (e.g., Ethereal, Urban, Alt-Rock) and your emotional resonance.
- 🤖 **Pluggable AI Engine**: Supports multiple models including **Gemini 2.5 Pro**, OpenAI, and Claude.
- 🌉 **Cross-Cultural Mapping**: Find English songs that share the same "musical DNA" as your favorite MandoPop divas.
- 🎤 **Pure Artist Mode / 100% Purity**: Generate playlists exclusively featuring a single artist (e.g., 100% Faye Wong).
- 🚀 **Full Automation**: Fetching, analyzing, and playlist creation—all in one click.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **AI Engine**: Google Gemini 2.5 Pro API
- **Data Source**: YouTube Data API v3
- **Validation**: Pydantic V2
- **Auth**: OAuth 2.0 (Google SDK)

## 🚀 Quick Start

### 1. Credentials Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/), create a project, and enable **YouTube Data API v3**.
2. Download `client_secrets.json` to the root directory.
3. Get your **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).

### 2. Install & Run
```bash
# Clone the repo
git clone https://github.com/<YOUR_GITHUB_USERNAME>/ai-music-curator.git
cd ai-music-curator

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `config/settings.yaml` file with the following structure:

```yaml
# AI Model Selection
active_ai_model: "gemini" 

# Target Language for recommendations (Mandarin / English)
recommendation_language: "Mandarin"

# Source Playlist ID (can be retrieved by running src/list_playlists.py)
source_playlist_id: "<YOUR_PLAYLIST_ID>"

# Singer Special Mode
# Leave empty "" for general discovery, or enter a name for a focused list
target_singer: "Faye Wong"

# 100% Purity Mode
# If true, all 15 songs will be by the target_singer
pure_artist_mode: true

# API Keys
gemini_api_key: "YOUR_GEMINI_API_KEY"
openai_api_key: ""
anthropic_api_key: ""
```

### 4. Execution
```bash
python src/fetch_liked_songs.py  # 1. Fetch Likes
python src/main.py               # 2. AI Analysis & Recommendation
python src/create_playlist.py    # 3. Create Playlist on YouTube
```

## 📂 Project Structure
- `src/fetch_liked_songs.py`: Interacts with YouTube API to fetch user tastes.
- `src/providers/`: Modular AI provider implementations.
- `src/main.py`: Core logic for taste analysis and recommendation generation.
- `src/create_playlist.py`: Searches and adds songs to YouTube playlists.
- `src/list_playlists.py`: Diagnostic tool for listing user playlists.

## 📝 Disclaimer
This project is for personal educational and research purposes only. Please adhere to the YouTube API Terms of Service.

---
*Made with ❤️ for MandoPop lovers.*
