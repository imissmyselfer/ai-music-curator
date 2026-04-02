import google.generativeai as genai
import json
from typing import List, Dict
from .base import BaseAIProvider, RecommendationOutput

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    def analyze_and_recommend(self, user_liked_songs: List[Dict], target_lang: str) -> RecommendationOutput:
        # Convert liked songs to string
        songs_str = "\n".join([f"- {s['title']} by {s['artist']}" for s in user_liked_songs])

        # Determine recommendation strategy based on target language
        if target_lang.lower() == "english":
            goal = "Recommend 15 'cross-cultural' English songs, finding Western tracks with styles similar to my favorite Mandarin artists. Prefer modern Indie Folk English artists."
            example = "If I like Faye Wong, recommend Cocteau Twins; if I like Stefanie Sun, recommend 90s Female Rock."
        else:
            goal = "Recommend 15 'Mandarin Pop' songs, deeply exploring other Mandarin artists with styles similar to my favorite singers."
            example = "If I like Faye Wong, recommend Sandee Chan or Faith Yang; if I like Stefanie Sun, recommend Cheer Chen or Penny Tai."

        prompt = f"""
        You are a senior music critic with high expertise in global pop music (especially the Mandarin music scene). Here are some Mandarin songs I've recently liked on YouTube Music:
        {songs_str}

        Task Goal: {goal}

        Please perform the following analysis:
        1. Style Parsing: Analyze the common attributes of these artists I like (e.g., Faye Wong, Stefanie Sun, Karen Mok) such as ethereal, alternative, urban, or rock vibes.
        2. Finding Connections: {example}

        Please return strictly in the following JSON format, without any extra text:
        {{
            "playlist_title": "AI Recommendation: [A title corresponding to the taste]",
            "recommendations": [
                {{ "artist": "Artist Name", "song_name": "Song Name", "reason": "Explain the stylistic connection between this recommended song and my original favorite Mandarin artists" }},
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
        
        # Parse and convert to Pydantic model
        data = json.loads(response.text)
        return RecommendationOutput(**data)

    def recommend_by_singer(self, singer_name: str, target_lang: str, pure_mode: bool = False) -> RecommendationOutput:
        """Perform 'Singer Special' recommendation for a single artist"""
        
        # Determine language version
        lang_str = "Mandarin" if target_lang.lower() != "english" else "English"
        
        # Determine purity requirement
        if pure_mode:
            purity_requirement = f"⚠️ Core Requirement: These 15 songs [MUST all be performed by {singer_name}]. Include both popular hits and deep cuts."
        else:
            purity_requirement = f"Recommend 15 songs. These songs can be by {singer_name} themselves, or by 'other artists with the exact same musical DNA'."

        prompt = f"""
        You are a senior music critic with deep research into global pop music (especially the Mandarin music scene). I am the #1 fan of [{singer_name}].
        
        Task:
        1. Deeply deconstruct the musical soul of [{singer_name}] (e.g., singing style, representative arrangement style, emotional delivery).
        2. {purity_requirement}
        3. These songs must cater to the tastes of '{lang_str}' fans.
        
        Please return strictly in JSON format:
        {{
            "playlist_title": "AI Exclusive: [A title that perfectly matches the aura of {singer_name}]",
            "recommendations": [
                {{ "artist": "{singer_name}", "song_name": "Song Name", "reason": "Analyze the unique significance of this song in {singer_name}'s career or its musical essence" }},
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
