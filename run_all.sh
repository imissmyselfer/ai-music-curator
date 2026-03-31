#!/bin/bash

# 進入虛擬環境
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "🎵 步驟 1: 抓取你的最新播放清單資料..."
python src/fetch_liked_songs.py

echo -e "\n🤖 步驟 2: AI 分析品味並產出推薦..."
python src/main.py

echo -e "\n✨ 步驟 3: 在 YouTube 上自動建立歌單並加入歌曲..."
python src/create_playlist.py

echo -e "\n🎉 全部完成！去 YouTube Music 聽聽看 AI 為你準備的驚喜吧！"
