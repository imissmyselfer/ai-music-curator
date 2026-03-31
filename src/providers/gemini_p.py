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

    def recommend_by_singer(self, singer_name: str, target_lang: str, pure_mode: bool = False) -> RecommendationOutput:
        """針對單一歌手進行『歌手專場』推薦"""
        
        # 決定語言版本
        lang_str = "Mandarin" if target_lang.lower() != "english" else "English"
        
        # 決定純度要求
        if pure_mode:
            purity_requirement = f"⚠️ 核心要求：這 15 首歌【必須全部都是由 {singer_name} 演唱】的作品。包含熱門金曲與隱藏神曲 (Deep Cuts)。"
        else:
            purity_requirement = f"推薦 15 首歌曲。這些歌曲可以是 {singer_name} 本人的歌，也可以是『其他歌手但具備完全相同音樂基因』的作品。"

        prompt = f"""
        你是一位對全球流行音樂（特別是華語樂壇）有極深研究的資深樂評人。我是【{singer_name}】的頭號歌迷。
        
        任務：
        1. 深度拆解【{singer_name}】的音樂魂（例如：唱法特色、代表性編曲風格、情感傳遞方式）。
        2. {purity_requirement}
        3. 這些歌曲必須符合『{lang_str}』歌迷的口味。
        
        請嚴格遵守 JSON 格式回傳：
        {{
            "playlist_title": "AI 專屬：[取一個與 {singer_name} 氣質完全吻合的標題]",
            "recommendations": [
                {{ "artist": "{singer_name}", "song_name": "歌名", "reason": "分析這首歌在 {singer_name} 演藝生涯中的獨特意義或其音樂神韻" }},
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
        
        data = json.loads(response.text)
        return RecommendationOutput(**data)
