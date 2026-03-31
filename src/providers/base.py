from abc import ABC, abstractmethod
from typing import List, Dict
from pydantic import BaseModel

class SongRecommendation(BaseModel):
    artist: str
    song_name: str
    reason: str

class RecommendationOutput(BaseModel):
    playlist_title: str
    recommendations: List[SongRecommendation]

class BaseAIProvider(ABC):
    @abstractmethod
    def analyze_and_recommend(self, user_liked_songs: List[Dict], target_lang: str) -> RecommendationOutput:
        """根據用戶喜歡的歌曲列表，回傳結構化的推薦結果"""
        pass

    @abstractmethod
    def recommend_by_singer(self, singer_name: str, target_lang: str, pure_mode: bool = False) -> RecommendationOutput:
        """針對特定歌手的風格進行專場推薦"""
        pass

