# 🎵 AI-Music-Curator (AI 華語音樂館長)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AI Model](https://img.shields.io/badge/AI_Model-Gemini_1.5_Pro-purple.svg)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **「從王菲的空靈到孫燕姿的倔強，讓 AI 讀懂你的音樂靈魂。」**

這是一個基於 AI 技術的華語流行音樂 (MandoPop) 推薦工具。它能深度分析你在 YouTube Music 中的「喜歡的歌曲」，並透過 Google Gemini 1.5 Pro 的強大語意理解能力，為你發掘靈魂相近的音樂，並自動在你的帳號中建立專屬播放清單。

## ✨ 核心亮點

- 🎧 **品味深度分析**：不只是標籤比對，AI 會分析歌手的氣質（如：空靈、都市感、另類搖滾）與你的情感共鳴。
- 🤖 **可插拔 AI 引擎**：支援 **Gemini 1.5 Pro**, OpenAI, Claude 等多種模型切換。
- 🚀 **完全自動化**：從抓取喜好、AI 推薦到建立 YouTube 歌單，一鍵完成。
- 🎹 **專注華語女伶**：特別優化對王菲、孫燕姿、莫文蔚等經典華語女聲的風格解析。

## 🛠️ 技術棧

- **語言**: Python 3.10+
- **AI 推薦**: Google Gemini 1.5 Pro API
- **資料獲取**: YouTube Data API v3
- **資料驗證**: Pydantic V2
- **授權管理**: OAuth 2.0 (Google SDK)

## 🚀 快速開始

### 1. 取得 API 憑證
1. 前往 [Google Cloud Console](https://console.cloud.google.com/) 建立專案並啟用 **YouTube Data API v3**。
2. 下載 `client_secrets.json` 放置於專案根目錄。
3. 前往 [Google AI Studio](https://aistudio.google.com/) 取得你的 **Gemini API Key**。

### 2. 安裝與執行
```bash
# 克隆專案
git clone git@github.com:imissmyselfer/ai-music-curator.git
cd ai-music-curator

# 安裝套件
pip install -r requirements.txt

# 設定 API Key
# 在 config/settings.yaml 中填入你的 Gemini API Key

# 執行三部曲
python src/fetch_liked_songs.py  # 1. 抓取喜好
python src/main.py               # 2. AI 分析與推薦
python src/create_playlist.py    # 3. 建立 YouTube 歌單
```

## 📂 專案架構
- `src/fetch_liked_songs.py`: 與 YouTube API 互動，抓取用戶喜歡的歌曲。
- `src/providers/`: AI 模型提供商模組，可輕鬆擴展不同 AI 模型。
- `src/main.py`: 核心邏輯，分析品味並產生推薦 JSON。
- `src/create_playlist.py`: 在 YouTube 上搜尋歌曲並自動建立播放清單。

## 📝 免責聲明
本專案僅供個人學習與研究使用，請遵守 YouTube API 的使用規範。

---
*Made with ❤️ for MandoPop lovers.*
