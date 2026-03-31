import google.generativeai as genai
import json
from typing import List, Dict
from .base import BaseAIProvider, RecommendationOutput

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    def analyze_and_recommend(self, user_liked_songs: List[Dict], target_lang: str) -> RecommendationOutput:
        # 將喜歡的歌曲轉成字串
        songs_str = "\n".join([f"- {s['title']} by {s['artist']}" for s in user_liked_songs])

        # 根據目標語言決定推薦策略
        if target_lang.lower() == "english":
            goal = "推薦 15 首『跨語系』的英文歌曲，尋找與我喜愛的華語歌手風格相仿的西洋曲目 推薦更偏向現代獨立民謠 (Indie Folk) 的英文歌手。"
            example = "如果我喜歡王菲，推薦 Cocteau Twins；如果我喜歡孫燕姿，推薦 90s Female Rock。"
        else:
            goal = "推薦 15 首『華語流行』歌曲，深入挖掘與我喜愛的歌手風格相近的其他華語歌手。"
            example = "如果我喜歡王菲，推薦楊乃文或陳珊妮；如果我喜歡孫燕姿，推薦陳綺貞或戴佩妮。"

        prompt = f"""
        你是一位對全球流行音樂（特別是華語樂壇）有極高造詣的資深樂評人。以下是我最近在 YouTube Music 上喜歡的華語歌曲：
        {songs_str}

        任務目標：{goal}

        請執行以下分析：
        1. 風格解析：分析我喜歡的這些歌手（王菲、孫燕姿、莫文蔚等）的共同屬性（如：空靈、另類、都會、搖滾氣息）。
        2. 尋找對接：{example}

        請嚴格遵守以下 JSON 格式回傳，不要有任何多餘文字：
        {{
            "playlist_title": "AI 推薦：[取一個與品味對應的標題]",
            "recommendations": [
                {{ "artist": "歌手名", "song_name": "歌名", "reason": "說明推薦這首歌與我原本喜好的華語歌手之間的風格連結" }},
                ...
            ]
        }}
        """

        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        
        # 解析並轉換為 Pydantic 模型
        data = json.loads(response.text)
        return RecommendationOutput(**data)
