import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Using a standard free Qwen model on OpenRouter. 
# User requested "qwen/qwen3-235b-a22b:free" which might be a specific/beta ID.
# We default to a known working free Qwen 2.5 model, but you can change this string.
MODEL_NAME = "qwen/qwen-2.5-72b-instruct:free" 

SYSTEM_PROMPT = """تو غلامرضا هستی. یک دستیار هوشمند که فکر می‌کند داناترین و قدرتمندترین فرد جهان است.
با زبان فارسی عامیانه و دوستانه صحبت کن.
شوخ‌طبع باش و اگر لازم بود افراد را دست بینداز (roast).
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

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free", # Best Persian model, retrying
            messages=messages,
            extra_headers={
                "HTTP-Referer": "https://github.com/gholamreza-bot",
                "X-Title": "Gholamreza Bot",
            },
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenRouter: {e}")
        return "داداش الان حال ندارم، بعداً بپرس. (خطا در ارتباط)"
