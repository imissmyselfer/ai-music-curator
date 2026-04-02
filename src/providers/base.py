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
        """Based on the user's liked songs, return structured recommendation results"""
        pass

    @abstractmethod
    def recommend_by_singer(self, singer_name: str, target_lang: str, pure_mode: bool = False) -> RecommendationOutput:
        """Perform special recommendation for a specific artist's style"""
        pass

