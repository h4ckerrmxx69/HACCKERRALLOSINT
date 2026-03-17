import telebot
import requests
import json
import os
from telebot import types

# --- CONFIGURATION ---
# @BotFather se mila hua token yahan daalein
API_TOKEN = "8411017661:AAHDO1JNiF6MVDQ5MlQlbY1hFBpVuggE_Ys"
bot = telebot.TeleBot(API_TOKEN)

# Headers taaki API server block na kare
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- API MAPPING (First Image ke hisaab se) ---
APIS = {
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🇵🇰 Pak Phone": "https://abbas-apis.vercel.app/api/pakistan?number={}",
    "🆔 Aadhaar Lookup": "https://aadhar.ek4nsh.in/?name={}",
    "👥 Family Info": "https://source-code-api.vercel.app/?num={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?code={}",
    "🏦 IFSC Old": "https://abbas-apis.vercel.app/api/ifsc?ifsc={}",
    "🌐 IP Lookup": "http://ip-api.com/json/{}",
    "📞 TG Number": "https://abbas-apis.vercel.app/api/github?username={}", # Image me TG tha but API Github ki thi
    "🐙 GitHub Profile": "https://abbas-apis.vercel.app/api/github?username={}",
    "📧 Email Lookup": "https://abbas-apis.vercel.app/api/email?mail={}",
    "💳 BIN Lookup": "https://lookup.binlist.net/{}",
    "📱 IMEI Lookup": "https://api.b77bf911.workers.dev/bin?bin={}",
    "🚗 Vehicle Num": "https://new-vehicle-api-eosin.vercel.app/vehicle?rc={}",
    "🎮 FreeFire ID": "https://abbas-apis.vercel.app/api/ff-info?uid={}",
    "🚫 FF Ban Check": "https://abbas-apis.vercel.app/api/ff-ban?uid={}",
    "🔍 Domain/Whois": "https://api.b77bf911.workers.dev/whois?domain={}"
}

user_state = {}

# /start command - Menu button dikhayega
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # ReplyKeyboardMarkup jo typing area ke neeche rahega
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Buttons add karna
    buttons = [types.KeyboardButton(name) for name in APIS.keys()]
    markup.add(*buttons)
    
    user_name = message.from_user.first_name if message.from_user.first_name else "User"
    bot.send_message(
        message.chat.id, 
        f"👋 Welcome *{user_name}*\n\nNeeche diye gaye menu se lookup select karein 👇",
        reply_markup=markup,
        parse_mode='Markdown'
    )

# Menu button click handle karna
@bot.message_handler(func=lambda message: message.text in APIS.keys())
def handle_menu_click(message):
    chat_id = message.chat.id
    user_state[chat_id] = message.text
    bot.send_message(
        chat_id, 
        f"🔍 Selected: *{message.text}*\n\nAb apni query (Number/ID/User) bhejein:",
        parse_mode='Markdown'
    )

# API Request aur Result handle karna
@bot.message_handler(func=lambda message: True)
def process_lookup(message):
    chat_id = message.chat.id
    query_text = message.text
    
    # Agar user ne bina button dabaye text bhej diya
    if chat_id not in user_state:
        bot.send_message(chat_id, "⚠️ Pehle neeche menu se koi option select karein!")
        return

    selected_option = user_state[chat_id]
    wait_msg = bot.send_message(chat_id, f"⏳ Searching *{query_text}* in *{selected_option}*...")
    
    try:
        # API URL banana
        url = APIS[selected_option].format(query_text)
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            try:
                # Raw JSON parse karna
                raw_data = response.json()
                pretty_json = json.dumps(raw_data, indent=2, ensure_ascii=False)
                
                # Check message length (Telegram limit 4096)
                if len(pretty_json) > 4000:
                    filename = f"result_{chat_id}.json"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(pretty_json)
                    bot.send_document(chat_id, open(filename, "rb"), caption=f"📄 Result for {selected_option}")
                    bot.delete_message(chat_id, wait_msg.message_id)
                    os.remove(filename)
                else:
                    bot.edit_message_text(
                        f"✅ *Raw JSON Result:*\n\n```json\n{pretty_json}\n```",
                        chat_id, wait_msg.message_id,
                        parse_mode='Markdown'
                    )
            except json.JSONDecodeError:
                # Agar API ne HTML error bheja (Jaise 1016)
                bot.edit_message_text(
                    f"⚠️ *Server Error*\n\nAPI ne valid JSON nahi bheja. Shayad server down hai.\n\n*Raw:* `{response.text[:200]}`",
                    chat_id, wait_msg.message_id, parse_mode='Markdown'
                )
        else:
            bot.edit_message_text(f"❌ API Error: HTTP {response.status_code}", chat_id, wait_msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"⚠️ Error: {str(e)}", chat_id, wait_msg.message_id)
    
    # State clear karna taaki naya lookup ho sake
    del user_state[chat_id]

print("Bot is live with all 16 APIs...")
bot.infinity_polling()
