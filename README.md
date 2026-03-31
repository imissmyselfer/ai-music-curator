# 🎵 AI-Music-Curator (AI 華語音樂館長)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AI Model](https://img.shields.io/badge/AI_Model-Gemini_2.5_Pro-purple.svg)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **「From the ethereal voice of Faye Wong to the resilient spirit of Stefanie Sun, let AI understand your musical soul.」**  
> **「從王菲的空靈到孫燕姿的倔強，讓 AI 讀懂你的音樂靈魂。」**

AI-Music-Curator is an intelligent MandoPop recommendation tool powered by AI. It analyzes your "Liked Songs" from YouTube Music and leverages Google Gemini 2.5 Pro's deep semantic understanding to discover kindred musical spirits and automatically generate curated playlists in your account.

這是一個基於 AI 技術的華語流行音樂 (MandoPop) 推薦工具。它能深度分析你在 YouTube Music 中的「喜歡的歌曲」，並透過 Google Gemini 2.5 Pro 的強大語意理解能力，為你發掘靈魂相近的音樂，並自動在你的帳號中建立專屬播放清單。

---

## ✨ Core Highlights / 核心亮點

- 🎧 **Deep Taste Analysis / 品味深度分析**: Beyond simple tags, AI analyzes the artist's essence (e.g., Ethereal, Urban, Alt-Rock) and your emotional resonance.  
  不只是標籤比對，AI 會分析歌手的氣質（如：空靈、都市感、另類搖滾）與你的情感共鳴。
- 🤖 **Pluggable AI Engine / 可插拔 AI 引擎**: Supports multiple models including **Gemini 2.5 Pro**, OpenAI, and Claude.  
  支援 **Gemini 2.5 Pro**, OpenAI, Claude 等多種模型切換。
- 🌉 **Cross-Cultural Mapping / 跨語系靈感橋樑**: Find English songs that share the same "musical DNA" as your favorite MandoPop divas.  
  尋找與你喜愛的華語女伶靈魂相近的英文歌曲。
- 🎤 **Pure Artist Mode / 100% 純度專場**: Generate playlists exclusively featuring a single artist (e.g., 100% Faye Wong).  
  針對特定歌手打造專屬歌單（如：100% 王菲專場）。
- 🚀 **Full Automation / 完全自動化**: Fetching, analyzing, and playlist creation—all in one click.  
  從抓取喜好、AI 推薦到建立 YouTube 歌單，一鍵完成。

## 🛠️ Tech Stack / 技術棧

- **Language / 語言**: Python 3.10+
- **AI Engine / AI 推薦**: Google Gemini 2.5 Pro API
- **Data Source / 資料獲取**: YouTube Data API v3
- **Validation / 資料驗證**: Pydantic V2
- **Auth / 授權管理**: OAuth 2.0 (Google SDK)

## 🚀 Quick Start / 快速開始

### 1. Credentials Setup / 取得憑證
1. Go to [Google Cloud Console](https://console.cloud.google.com/), create a project, and enable **YouTube Data API v3**.  
   前往 Google Cloud Console 建立專案並啟用 YouTube Data API v3。
2. Download `client_secrets.json` to the root directory.  
   下載 `client_secrets.json` 放置於專案根目錄。
3. Get your **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).  
   前往 Google AI Studio 取得你的 Gemini API Key。

### 2. Install & Run / 安裝與執行
```bash
# Clone the repo / 複製專案
git clone https://github.com/<YOUR_GITHUB_USERNAME>/ai-music-curator.git
cd ai-music-curator

# Install dependencies / 安裝套件
pip install -r requirements.txt
```

### 3. Configuration / 設定
Create a `config/settings.yaml` file with the following structure:  
請建立 `config/settings.yaml` 並參考以下設定：

```yaml
# AI Model Selection / AI 模型選擇
active_ai_model: "gemini" 

# Target Language for recommendations / 推薦語言 (Mandarin / English)
recommendation_language: "Mandarin"

# Source Playlist ID (e.g., from src/list_playlists.py)
# 來源播放清單 ID (可透過執行 src/list_playlists.py 取得)
source_playlist_id: "<YOUR_PLAYLIST_ID>"

# Singer Special Mode / 歌手專場模式
# Leave empty "" for general discovery, or enter a name for a focused list
# 留空則進行綜合分析，填入姓名則針對該歌手進行推薦
target_singer: "王菲"

# 100% Purity Mode / 100% 純度模式
# If true, all 15 songs will be by the target_singer
# 若為 true，則歌單內 15 首歌將全部為該歌手的作品
pure_artist_mode: true

# API Keys
gemini_api_key: "YOUR_GEMINI_API_KEY"
openai_api_key: ""
anthropic_api_key: ""
```

### 4. Execution / 執行三部曲
```bash
python src/fetch_liked_songs.py  # 1. Fetch Likes / 抓取喜好
python src/main.py               # 2. AI Analysis / AI 分析與推薦
python src/create_playlist.py    # 3. Create Playlist / 建立 YouTube 歌單
```

## 📂 Project Structure / 專案架構
- `src/fetch_liked_songs.py`: Interacts with YouTube API to fetch user tastes. / 與 YouTube API 互動，抓取用戶喜好。
- `src/providers/`: Modular AI provider implementations. / AI 模型提供商模組，可輕鬆擴展。
- `src/main.py`: Core logic for taste analysis and recommendation generation. / 核心邏輯，分析品味並產生推薦。
- `src/create_playlist.py`: Searches and adds songs to YouTube playlists. / 在 YouTube 上搜尋歌曲並自動建立播放清單。
- `src/list_playlists.py`: Diagnostic tool for listing user playlists. / 播放清單診斷工具。

## 📝 Disclaimer / 免責聲明
This project is for personal educational and research purposes only. Please adhere to the YouTube API Terms of Service.  
本專案僅供個人學習與研究使用，請遵守 YouTube API 的使用規範。

---
*Made with ❤️ for MandoPop lovers.*
