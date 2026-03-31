import os
import json
import yaml
from providers.gemini_p import GeminiProvider
# from providers.openai_p import OpenAIProvider  # 之後可以擴展
# from providers.ollama_p import OllamaProvider

def load_config():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    # 1. 載入配置與喜歡的歌曲
    config = load_config()
    with open("data/liked_songs.json", "r", encoding="utf-8") as f:
        liked_songs = json.load(f)

    print(f"✅ 已載入 {len(liked_songs)} 首喜歡的歌曲資料。")

    # 2. 初始化 AI 提供商
    active_model = config.get("active_ai_model", "gemini")
    target_lang = config.get("recommendation_language", "Mandarin")
    
    if active_model == "gemini":
        api_key = os.getenv("GEMINI_API_KEY") or config.get("gemini_api_key")
        if not api_key:
            print("❌ 錯誤: 找不到 GEMINI_API_KEY。")
            return
        provider = GeminiProvider(api_key)
    else:
        print(f"❌ 錯誤: 目前尚未實作 {active_model} 模型。")
        return

    # 3. 執行分析與推薦
    target_singer = config.get("target_singer", "")
    pure_mode = config.get("pure_artist_mode", False)
    
    try:
        if target_singer:
            mode_text = "純度 100%" if pure_mode else "風格相近"
            print(f"🎤 正在為你準備『{target_singer}』專場推薦 ({mode_text} - {target_lang})...")
            output = provider.recommend_by_singer(target_singer, target_lang, pure_mode)
        else:
            print(f"🤖 正在根據你的 {len(liked_songs)} 首收藏進行『{target_lang}』綜合推薦...")
            output = provider.analyze_and_recommend(liked_songs, target_lang)
        
        # 4. 展示與儲存結果
        print(f"\n✨ AI 產出的歌單標題：{output.playlist_title}")
        print("-" * 50)
        
        for i, rec in enumerate(output.recommendations, 1):
            print(f"{i}. {rec.song_name} - {rec.artist}")
            print(f"   💡 原因：{rec.reason}\n")
            
        # 5. 存檔推薦結果
        with open("data/recommendations.json", "w", encoding="utf-8") as f:
            json.dump(output.model_dump(), f, ensure_ascii=False, indent=2)
        print(f"📂 推薦清單已存至: data/recommendations.json")

    except Exception as e:
        print(f"❌ 執行過程中發生錯誤: {e}")

if __name__ == "__main__":
    main()
