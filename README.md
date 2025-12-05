# Gholamreza Telegram Bot

This is a Telegram bot acting as a Persian AI assistant named "Gholamreza".

## Features
- **Persona:** Gholamreza, the most knowledgeable and powerful man in the world (comedy/roast style).
- **Model:** Uses OpenRouter (Qwen).
- **Access Control:** 
  - DMs only work for the owner (ID: 90441478).
  - Group chats must be explicitly enabled by the owner.
- **Triggers:**
  - Starts with "غلامرضا" or "غلام رضا".
  - Replies to the bot.
  - Replies to others where the reply starts with "غلامرضا".

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables:**
    - Copy `.env.example` to a new file named `.env`.
    - Fill in your `TELEGRAM_BOT_TOKEN` and `OPENROUTER_API_KEY`.

3.  **Run:**
    ```bash
    python bot.py
    ```

## Commands
- `/start`: Start the bot.
- `/enable`: Enable the bot in the current group (Owner only).
- `/disable`: Disable the bot in the current group (Owner only).
