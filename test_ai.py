import asyncio
import os
from dotenv import load_dotenv
from ai_client import get_ai_response

# Load environment variables
load_dotenv()

async def test_ai():
    print("Testing connection to OpenRouter...")
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in .env")
        return

    print(f"API Key found: {api_key[:5]}...")
    
    print("Sending message: 'سلام غلامرضا، حالت چطوره؟'")
    response = await get_ai_response("سلام غلامرضا، حالت چطوره؟")
    
    print("-" * 20)
    print("Response from Gholamreza:")
    print(response)
    print("-" * 20)

if __name__ == "__main__":
    asyncio.run(test_ai())
