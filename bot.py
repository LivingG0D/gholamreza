import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telegram.request import HTTPXRequest
from dotenv import load_dotenv
from chat_manager import ChatManager
from ai_client import get_ai_response

# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
_owner_id_str = os.getenv("OWNER_ID")
OWNER_ID = int(_owner_id_str) if _owner_id_str else None

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize Chat Manager
chat_manager = ChatManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("به نام خدا. من غلامرضا هستم. امر بفرمایید؟")

async def enable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    print(f"Debug: /enable called by user_id={user.id} in chat_id={chat.id}. Owner ID is {OWNER_ID}")

    if user.id != OWNER_ID:
        await update.message.reply_text(f"شما اجازه ندارید. (ID شما: {user.id})")
        return

    if chat.type in ['group', 'supergroup']:
        if chat_manager.enable_chat(chat.id):
            await update.message.reply_text("حله رئیس، اینجا هم هستم.")
        else:
            await update.message.reply_text("اینجا که قبلاً فعال بود!")
    else:
        await update.message.reply_text("این دستور فقط مخصوص گروه‌هاست.")

async def disable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    if user.id != OWNER_ID:
        return # Silent ignore for non-owners

    if chat.type in ['group', 'supergroup']:
        if chat_manager.disable_chat(chat.id):
            await update.message.reply_text("خداحافظ، من رفتم.")
        else:
            await update.message.reply_text("اینجا که اصلا فعال نبودم!")
    else:
        await update.message.reply_text("این دستور فقط مخصوص گروه‌هاست.")

def should_respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return False

    text = message.text.strip()
    is_private = update.effective_chat.type == 'private'
    is_owner = update.effective_user.id == OWNER_ID
    chat_id = update.effective_chat.id

    # Rule 1: Direct Messages (Private)
    if is_private:
        return is_owner # Only owner can use in DM

    # Rule 2: Group Chats
    if not chat_manager.is_enabled(chat_id):
        return False

    # Triggers
    starts_with_name = text.startswith("غلامرضا") or text.startswith("غلام رضا")
    is_reply = message.reply_to_message is not None
    
    if starts_with_name:
        return True
    
    if is_reply:
        # Check if from_user exists (it might be None for channels/anonymous admins)
        if message.reply_to_message.from_user:
            replied_user_id = message.reply_to_message.from_user.id
            bot_id = context.bot.id
            
            # Reply to Bot
            if replied_user_id == bot_id:
                return True
            
    return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not should_respond(update, context):
        # If private and not owner, maybe tell them off? 
        # Instructions said "it shouldnt answer anything in direct messages exept me".
        # So silent ignore is correct.
        return

    message = update.message
    text = message.text
    
    # Prepare context for AI
    ai_context = []
    prompt_text = text

    # Handle Reply Context
    if message.reply_to_message and message.reply_to_message.text:
        replied_text = message.reply_to_message.text
        
        # Determine replied user name safely
        if message.reply_to_message.from_user:
            replied_user = message.reply_to_message.from_user.first_name or "کاربر"
            replied_user_id = message.reply_to_message.from_user.id
        else:
            replied_user = "کانال/ناشناس"
            replied_user_id = None
        
        # If replying to bot, treat it as conversation history
        if replied_user_id == context.bot.id:
            ai_context.append({"role": "assistant", "content": replied_text})
        else:
            # If replying to someone else, provide that context
            # Prompt: "answer the question about the replied message of someone else"
            # We inject the replied message as context or part of the prompt
            prompt_text = f"کاربر به این پیام اشاره کرده: '{replied_text}' از {replied_user}. \n\nپیام کاربر: {text}"

    # Clean up trigger word from prompt if it's just a direct call
    # But for "personality", keeping it might be fine. 
    # The prompt says "answer brief answers to whoever starts his message with غلامرضا"
    # Let's just pass the whole text, the AI handles the name.

    # Send 'typing' action
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    # Get AI Response
    response = await get_ai_response(prompt_text, ai_context)
    
    # Reply
    await message.reply_text(response, quote=True)

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables.")
        exit(1)
    
    if not OWNER_ID:
        print("Error: OWNER_ID not found in environment variables.")
        exit(1)
    
    # Check for proxy
    proxy_url = os.getenv("TELEGRAM_PROXY_URL")
    
    # Configure request with longer timeouts and proxy if available
    request_kwargs = {'connect_timeout': 30.0, 'read_timeout': 30.0}
    if proxy_url:
        request_kwargs['proxy'] = proxy_url  # Use 'proxy' instead of deprecated 'proxy_url'

    request = HTTPXRequest(**request_kwargs)
    
    builder = ApplicationBuilder().token(BOT_TOKEN).request(request)
    
    if proxy_url:
        print(f"Using proxy: {proxy_url}")

    application = builder.build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('enable', enable))
    application.add_handler(CommandHandler('disable', disable))
    
    # Text message handler
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Gholamreza Bot started...")
    application.run_polling()
