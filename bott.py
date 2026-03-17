import telebot
import requests
import json
import os
import time
from telebot import types

# --- CONFIGURATION ---
# @BotFather se naya token lekar yahan daalein
API_TOKEN = "8411017661:AAFYSg_0ATzf-sPmoj-it77t3pp_4RAyWUg"
bot = telebot.TeleBot(API_TOKEN)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- ALL APIS (As per Image + New Num Trace) ---
APIS = {
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🇵🇰 Pak Phone": "https://abbas-apis.vercel.app/api/pakistan?number={}",
    "🆔 Aadhaar Lookup": "https://aadhar.ek4nsh.in/?name={}",
    "🚗 Vehicle Num": "https://new-vehicle-api-eosin.vercel.app/vehicle?rc={}",
    "💳 BIN Lookup": "https://lookup.binlist.net/{}",
    "💳 BIN New": "https://api.b77bf911.workers.dev/bin?bin={}",
    "🌐 IP Lookup": "http://ip-api.com/json/{}",
    "🐙 GitHub Profile": "https://abbas-apis.vercel.app/api/github?username={}",
    "📧 Email Lookup": "https://abbas-apis.vercel.app/api/email?mail={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?code={}",
    "🏦 IFSC Old": "https://abbas-apis.vercel.app/api/ifsc?ifsc={}",
    "🎮 FreeFire ID": "https://abbas-apis.vercel.app/api/ff-info?uid={}",
    "🚫 FF Ban Check": "https://abbas-apis.vercel.app/api/ff-ban?uid={}",
    "👥 Family Info": "https://source-code-api.vercel.app/?num={}",
    "👤 Num Owner": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🔍 Domain/Whois": "https://api.b77bf911.workers.dev/whois?domain={}",
    "📍 Num Trace": "https://ab-calltraceapi.vercel.app/info?number={}" # New API Added
}

user_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(name) for name in APIS.keys()]
    markup.add(*buttons)
    
    bot.send_message(
        message.chat.id, 
        "👋 *OSINT Bot Ready!*\n\nSaari APIs (17) set kar di gayi hain. Menu select karein 👇", 
        reply_markup=markup, 
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text in APIS.keys())
def handle_menu_click(message):
    user_state[message.chat.id] = message.text
    bot.send_message(
        message.chat.id, 
        f"🔍 Selected: *{message.text}*\n\nAb apni query (Number/ID/User) bhejein:", 
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def process_lookup(message):
    chat_id = message.chat.id
    selected_api = user_state[chat_id]
    query_text = message.text
    
    # If user clicks another button while waiting for input
    if query_text in APIS:
        user_state[chat_id] = query_text
        bot.send_message(chat_id, f"🔄 Switched to: *{query_text}*")
        return

    wait_msg = bot.send_message(chat_id, "⏳ Fetching Raw JSON Data...")
    
    try:
        # Construct URL and request
        url = APIS[selected_api].format(query_text)
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        try:
            # Parse and format JSON
            raw_data = response.json()
            pretty_json = json.dumps(raw_data, indent=2, ensure_ascii=False)
            
            # Telegram message length check
            if len(pretty_json) > 4000:
                filename = f"result_{chat_id}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(pretty_json)
                bot.send_document(chat_id, open(filename, "rb"), caption=f"📄 Result for {selected_api}")
                bot.delete_message(chat_id, wait_msg.message_id)
                os.remove(filename)
            else:
                bot.edit_message_text(
                    f"✅ *Raw JSON Result:*\n\n```json\n{pretty_json}\n```", 
                    chat_id, wait_msg.message_id, 
                    parse_mode='Markdown'
                )
        except:
            # Fallback for Non-JSON responses
            bot.edit_message_text(
                f"⚠️ *Server Response (Not JSON):*\n\n`{response.text[:1000]}`", 
                chat_id, wait_msg.message_id, 
                parse_mode='Markdown'
            )
            
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", chat_id, wait_msg.message_id)
    
    # Reset state
    if chat_id in user_state:
        del user_state[chat_id]

# --- 409 CONFLICT FIX ---
if __name__ == "__main__":
    print("Clearing webhooks and old sessions...")
    bot.remove_webhook()
    time.sleep(1)
    print("Bot is alive with all updated APIs!")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
