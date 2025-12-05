import asyncio
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    max_retries=0,
)

# Updated Dec 2025 - Valid free models on OpenRouter
MODELS_TO_TEST = [
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-4-scout:free",
    "meta-llama/llama-4-maverick:free",
    "deepseek/deepseek-r1:free",
    "qwen/qwen3-32b:free",
]

async def test_ai():
    print("Testing models to find a working one...")
    
    messages = [{"role": "user", "content": "Say 'Hello' in Persian."}]

    for model in MODELS_TO_TEST:
        print(f"Testing: {model}...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                extra_headers={
                    "HTTP-Referer": "https://github.com/gholamreza-bot",
                    "X-Title": "Gholamreza Bot",
                },
            )
            content = response.choices[0].message.content
            if content and content.strip():
                print(f"✅ SUCCESS with {model}!")
                print(f"Response: {content}")
                return
            else:
                print(f"❌ {model} returned empty response.")
        except Exception as e:
            print(f"❌ {model} failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai())