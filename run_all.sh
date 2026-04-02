#!/bin/bash

# Enter virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "🎵 Step 1: Fetching your latest liked songs data..."
python src/fetch_liked_songs.py

echo -e "\n🤖 Step 2: AI analyzing tastes and generating recommendations..."
python src/main.py

echo -e "\n✨ Step 3: Automatically creating playlist and adding songs on YouTube..."
python src/create_playlist.py

echo -e "\n🎉 All done! Go to YouTube Music and check out the surprise AI has prepared for you!"
