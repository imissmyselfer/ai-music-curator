import google.generativeai as genai
import json
from typing import List, Dict
from .base import BaseAIProvider, RecommendationOutput

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    def analyze_and_recommend(self, user_liked_songs: List[Dict], prompt_context: str) -> RecommendationOutput:
        # 將喜歡的歌曲轉成字串
        songs_str = "\n".join([f"- {s['title']} by {s['artist']}" for s in user_liked_songs])
        
        # 這是我們的核心提示詞 (Prompt Engineering)
        prompt = f"""
        你是一位對華語樂壇有深厚了解的資深樂評人。以下是我最近在 YouTube Music 上喜歡的歌曲清單：
        {songs_str}
        
        情境需求：{prompt_context}
        
        請執行以下任務：
        1. 分析我的音樂品味（例如：是否偏好空靈、另類搖滾、都市抒情等風格）。
        2. 根據這些風格，推薦 15 首『我還沒有在清單中』但極大機率會喜歡的華語流行歌曲。
        3. 推薦的歌曲應包含不同年代但靈魂相近的歌手。
        
        請嚴格遵守以下 JSON 格式回傳，不要有任何多餘的文字說明：
        {{
            "playlist_title": "AI 推薦：[這裡取一個有品味的名稱]",
            "recommendations": [
                {{ "artist": "歌手名", "song_name": "歌名", "reason": "推薦原因" }},
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
