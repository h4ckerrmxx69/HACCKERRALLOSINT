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

# --- ALL APIS (Organized for better visibility) ---
APIS = {
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "📍 Num Trace": "https://ab-calltraceapi.vercel.app/info?number={}", # Ab ye top pe dikhega
    "🇵🇰 Pak Phone": "https://abbas-apis.vercel.app/api/pakistan?number={}",
    "🆔 Aadhaar Lookup": "https://aadhar.ek4nsh.in/?name={}",
    "👥 Family Info": "https://source-code-api.vercel.app/?num={}",
    "👤 Num Owner": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🚗 Vehicle Num": "https://new-vehicle-api-eosin.vercel.app/vehicle?rc={}",
    "🌐 IP Lookup": "http://ip-api.com/json/{}",
    "🎮 FreeFire ID": "https://abbas-apis.vercel.app/api/ff-info?uid={}",
    "🚫 FF Ban Check": "https://abbas-apis.vercel.app/api/ff-ban?uid={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?code={}",
    "🏦 IFSC Old": "https://abbas-apis.vercel.app/api/ifsc?ifsc={}",
    "💳 BIN Lookup": "https://lookup.binlist.net/{}",
    "💳 BIN New": "https://api.b77bf911.workers.dev/bin?bin={}",
    "🐙 GitHub Profile": "https://abbas-apis.vercel.app/api/github?username={}",
    "📧 Email Lookup": "https://abbas-apis.vercel.app/api/email?mail={}",
    "🔍 Domain/Whois": "https://api.b77bf911.workers.dev/whois?domain={}"
}

user_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # ReplyKeyboardMarkup for the menu
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(name) for name in APIS.keys()]
    markup.add(*buttons)
    
    bot.send_message(
        message.chat.id, 
        "👋 *OSINT Bot Ready!*\n\nSaari 17 APIs (including Num Trace) set hain. Menu select karein 👇", 
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
    
    # Switch API if user clicks another menu button
    if query_text in APIS:
        user_state[chat_id] = query_text
        bot.send_message(chat_id, f"🔄 Switched to: *{query_text}*")
        return

    wait_msg = bot.send_message(chat_id, "⏳ Fetching Raw JSON Data...")
    
    try:
        url = APIS[selected_api].format(query_text)
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        try:
            # Format and send JSON
            raw_data = response.json()
            pretty_json = json.dumps(raw_data, indent=2, ensure_ascii=False)
            
            if len(pretty_json) > 4000:
                filename = f"res_{chat_id}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(pretty_json)
                bot.send_document(chat_id, open(filename, "rb"), caption=f"📄 Full Result for {selected_api}")
                bot.delete_message(chat_id, wait_msg.message_id)
                os.remove(filename)
            else:
                bot.edit_message_text(
                    f"✅ *Raw JSON Result:*\n\n```json\n{pretty_json}\n```", 
                    chat_id, wait_msg.message_id, 
                    parse_mode='Markdown'
                )
        except:
            # If API doesn't return JSON
            bot.edit_message_text(
                f"⚠️ *Server Response (Not JSON):*\n\n`{response.text[:1000]}`", 
                chat_id, wait_msg.message_id, 
                parse_mode='Markdown'
            )
            
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", chat_id, wait_msg.message_id)
    
    # Clear state for next lookup
    del user_state[chat_id]

if __name__ == "__main__":
    print("Fixing 409 Conflicts...")
    bot.remove_webhook()
    time.sleep(1)
    print("Bot is alive with 17 APIs!")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
