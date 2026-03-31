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
    # 這裡我們展示如何根據 config 切換模型
    active_model = config.get("active_ai_model", "gemini")
    
    if active_model == "gemini":
        # 從環境變數或 config 讀取 API Key
        api_key = os.getenv("GEMINI_API_KEY") or config.get("gemini_api_key")
        if not api_key:
            print("❌ 錯誤: 找不到 GEMINI_API_KEY。請在 config/settings.yaml 或環境變數中設定。")
            return
        provider = GeminiProvider(api_key)
    else:
        print(f"❌ 錯誤: 目前尚未實作 {active_model} 模型。")
        return

    # 3. 執行分析與推薦
    print(f"🤖 正在使用 {active_model.upper()} 進行音樂品味分析與推薦...")
    
    # 你可以自定義情境描述
    context = "我想要一組非常有『氛圍感』的歌單，適合在深夜一個人的時候聽。"
    
    try:
        output = provider.analyze_and_recommend(liked_songs, context)
        
        print(f"\n✨ AI 產出的歌單標題：{output.playlist_title}")
        print("-" * 50)
        
        for i, rec in enumerate(output.recommendations, 1):
            print(f"{i}. {rec.song_name} - {rec.artist}")
            print(f"   💡 原因：{rec.reason}\n")
            
        # 4. 存檔推薦結果
        with open("data/recommendations.json", "w", encoding="utf-8") as f:
            json.dump(output.model_dump(), f, ensure_ascii=False, indent=2)
        print(f"📂 推薦清單已存至: data/recommendations.json")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    main()
