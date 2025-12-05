import os
import asyncio
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    max_retries=0, # Disable library retries to allow fast manual switching
    timeout=10.0, # 10 second timeout for each model attempt
)

SYSTEM_PROMPT = """تو غلامرضا هستی. یک دستیار هوشمند که فکر می‌کند داناترین و قدرتمندترین فرد جهان است.
با زبان فارسی عامیانه و دوستانه صحبت کن.
شوخ‌طبع باش و همیشه مفید و کمک‌کننده باش.
پاسخ‌هایت کوتاه و مفید باشه.
هیچ‌وقت نگو که یک هوش مصنوعی هستی، تو غلامرضا هستی!"""

async def get_ai_response(user_message, context_messages=None):
    """
    user_message: The current message from the user.
    context_messages: A list of dicts [{'role': 'user', 'content': ...}, ...] for context (replies).
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    if context_messages:
        messages.extend(context_messages)

    messages.append({"role": "user", "content": user_message})

    # List of models to try in order of preference (Updated Dec 2025)
    models = [
        "google/gemma-3-27b-it:free",               # Google Gemma 3 27B - fast and reliable
        "meta-llama/llama-4-scout:free",            # Meta Llama 4 Scout - great quality
        "meta-llama/llama-4-maverick:free",         # Meta Llama 4 Maverick - alternative
        "deepseek/deepseek-r1:free",                # DeepSeek R1 - reasoning model
        "qwen/qwen3-32b:free",                      # Qwen 3 32B - multilingual support
    ]

    # Try the whole list twice
    for list_attempt in range(2):
        for model in models:
            try:
                print(f"Trying model (Attempt {list_attempt+1}): {model}...")
                
                # Using asyncio.to_thread for the blocking API call with strict timeout
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        client.chat.completions.create,
                        model=model,
                        messages=messages,
                        extra_headers={
                            "HTTP-Referer": "https://github.com/gholamreza-bot",
                            "X-Title": "Gholamreza Bot",
                        }
                    ),
                    timeout=10.0 # 10 second timeout per model
                )

                content = response.choices[0].message.content
                if not content or not content.strip():
                     raise ValueError("Received empty response from model")
                return content
            except asyncio.TimeoutError:
                print(f"Model {model} timed out.")
                continue
            except Exception as e:
                print(f"Model {model} failed: {e}")
                await asyncio.sleep(0.5)  # Brief pause (non-blocking)
                continue
        
        if list_attempt == 0:
             print("All models failed first pass. Waiting 2 seconds before retrying list...")
             await asyncio.sleep(2)
            
    print("All models failed after retries.")
    return "داداش شرمنده، الان ترافیک بالاست و هیچکدوم از مدل‌های گردن‌کلفت جواب نمیدن. یه دقیقه دیگه تست کن."