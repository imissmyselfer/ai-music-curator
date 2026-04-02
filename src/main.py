import os
import json
import yaml
from providers.gemini_p import GeminiProvider
# from providers.openai_p import OpenAIProvider  # Can be extended later
# from providers.ollama_p import OllamaProvider

def load_config():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    # 1. Load configuration and liked songs
    config = load_config()
    with open("data/liked_songs.json", "r", encoding="utf-8") as f:
        liked_songs = json.load(f)

    print(f"✅ Loaded {len(liked_songs)} liked songs data.")

    # 2. Initialize AI provider
    active_model = config.get("active_ai_model", "gemini")
    target_lang = config.get("recommendation_language", "Mandarin")
    
    if active_model == "gemini":
        api_key = os.getenv("GEMINI_API_KEY") or config.get("gemini_api_key")
        if not api_key:
            print("❌ Error: GEMINI_API_KEY not found.")
            return
        provider = GeminiProvider(api_key)
    else:
        print(f"❌ Error: {active_model} model is not implemented yet.")
        return

    # 3. Perform analysis and recommendation
    target_singer = config.get("target_singer", "")
    pure_mode = config.get("pure_artist_mode", False)
    
    try:
        if target_singer:
            mode_text = "100% Purity" if pure_mode else "Similar Style"
            print(f"🎤 Preparing special recommendation for '{target_singer}' ({mode_text} - {target_lang})...")
            output = provider.recommend_by_singer(target_singer, target_lang, pure_mode)
        else:
            print(f"🤖 Performing comprehensive '{target_lang}' recommendations based on your {len(liked_songs)} favorites...")
            output = provider.analyze_and_recommend(liked_songs, target_lang)
        
        # 4. Display and save results
        print(f"\n✨ AI-generated playlist title: {output.playlist_title}")
        print("-" * 50)
        
        for i, rec in enumerate(output.recommendations, 1):
            print(f"{i}. {rec.song_name} - {rec.artist}")
            print(f"   💡 Reason: {rec.reason}\n")
            
        # 5. Save recommendation results
        with open("data/recommendations.json", "w", encoding="utf-8") as f:
            json.dump(output.model_dump(), f, ensure_ascii=False, indent=2)
        print(f"📂 Recommendation list saved to: data/recommendations.json")

    except Exception as e:
        print(f"❌ Error occurred during execution: {e}")

if __name__ == "__main__":
    main()
