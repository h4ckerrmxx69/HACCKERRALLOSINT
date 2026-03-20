import telebot
import requests
import json
import os
import time
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = "8411017661:AAFYSg_0ATzf-sPmoj-it77t3pp_4RAyWUg"
ADMIN_ID = 5192884021  # <--- Apni numerical ID yahan daalein
bot = telebot.TeleBot(API_TOKEN)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- ALL APIS (Keyboard order mein set hain) ---
APIS = {
    "📸 Insta Lookup": "https://allnew.proportalxc.workers.dev/instagram?username={}",
    "🔍 GST Lookup": "https://paid.proportalxc.workers.dev/gst?gst={}",
    "📍 Pincode Search": "https://paid.proportalxc.workers.dev/pincode?pincode={}",
    "🌐 IP Detail": "https://paid.proportalxc.workers.dev/ip?ip={}",
    "🎮 FF Player Info": "http://203.57.85.58:2005/player-info?uid={}",
    "🚫 FF Ban Check": "http://203.57.85.58:2005/bancheck?uid={}",
    "📊 FF Level Check": "http://203.57.85.58:2005/level?uid={}",
    "🌍 FF Region": "http://203.57.85.58:2005/region?uid={}",
    "🎁 FF Wishlist": "http://203.57.85.58:2005/wishlist?uid={}",
    "🔍 FF Name Search": "http://203.57.85.58:2005/search?name={}",
    "🎫 FF Token Decode": "http://203.57.85.58:2005/decode?token={}",
    "📅 FF Events": "http://203.57.85.58:2005/events?region={}",
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "📍 Num Trace": "https://ab-calltraceapi.vercel.app/info?number={}",
    "🇵🇰 Pak Phone": "https://abbas-apis.vercel.app/api/pakistan?number={}",
    "🆔 Aadhaar Lookup": "https://aadhar.ek4nsh.in/?name={}",
    "👥 Family Info": "https://source-code-api.vercel.app/?num={}",
    "👤 Num Owner": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🚗 Vehicle Num": "https://new-vehicle-api-eosin.vercel.app/vehicle?rc={}",
    "📧 Email Lookup": "https://api.eva.pingutil.com/email?email={}",
    "🐙 GitHub Profile": "https://abbas-apis.vercel.app/api/github?username={}",
    "🔍 Domain/Whois": "https://api.b77bf911.workers.dev/whois?domain={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?code={}",
    "💳 BIN Lookup": "https://lookup.binlist.net/{}"
}

# --- EXAMPLES FOR ALL 24 TOOLS ---
EXAMPLES = {
    "📸 Insta Lookup": "Example: `physicswallah` (Username)",
    "🔍 GST Lookup": "Example: `07AAAAA0000A1Z5` (GSTIN Number)",
    "📍 Pincode Search": "Example: `110001` (6-digit Pincode)",
    "🌐 IP Detail": "Example: `8.8.8.8` (IPv4 Address)",
    "🎮 FF Player Info": "Example: `2919267964` (Numeric UID)",
    "🚫 FF Ban Check": "Example: `2919267964` (Numeric UID)",
    "📊 FF Level Check": "Example: `2919267964` (Numeric UID)",
    "🌍 FF Region": "Example: `2919267964` (Numeric UID)",
    "🎁 FF Wishlist": "Example: `2919267964` (Numeric UID)",
    "🔍 FF Name Search": "Example: `yash` (In-game Name)",
    "🎫 FF Token Decode": "Example: `eyJhbGci...` (JWT Token)",
    "📅 FF Events": "Example: `europe` or `indonesia` (Region)",
    "📱 Phone Lookup": "Example: `91XXXXXXXXXX` (With Country Code)",
    "📍 Num Trace": "Example: `92XXXXXXXXXX` (With CC)",
    "🇵🇰 Pak Phone": "Example: `03XXXXXXXXX` (Pakistan Number)",
    "🆔 Aadhaar Lookup": "Example: `Rajesh Kumar` (Full Name)",
    "👥 Family Info": "Example: `91XXXXXXXXXX` (Mobile Number)",
    "👤 Num Owner": "Example: `91XXXXXXXXXX` (Mobile Number)",
    "🚗 Vehicle Num": "Example: `DL10CE1234` (RC Number)",
    "📧 Email Lookup": "Example: `test@gmail.com` (Email Address)",
    "🐙 GitHub Profile": "Example: `hacker` (GitHub Username)",
    "🔍 Domain/Whois": "Example: `google.com` (Domain Name)",
    "🏦 IFSC Lookup": "Example: `SBIN0001234` (Bank IFSC Code)",
    "💳 BIN Lookup": "Example: `457173` (First 6 digits)"
}

user_state = {}
DEV_TAG = "\n\n━━━━━━━━━━━━━━━\n👤 **Developer:- @hackerrmx69**"

def send_long_message(chat_id, text):
    """Chunk system for long JSON results"""
    if len(text) <= 4096:
        bot.send_message(chat_id, text, parse_mode='Markdown')
    else:
        for i in range(0, len(text), 4000):
            bot.send_message(chat_id, text[i:i+4000])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(name) for name in APIS.keys()]
    markup.add(*buttons)
    bot.send_message(
        message.chat.id, 
        "💀 **H4CKERR MX Multi-Lookup V6.0**\n\nSaare tools keyboard mein set hain. Ek-ek example bhi add kar diya hai! 👇", 
        reply_markup=markup, 
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text in APIS.keys())
def handle_menu_click(message):
    service = message.text
    user_state[message.chat.id] = service
    instruction = EXAMPLES.get(service, "Apni query enter karein:")
    bot.send_message(
        message.chat.id, 
        f"🛠 **Tool Selected:** {service}\n📝 **Instruction:** {instruction}", 
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def process_lookup(message):
    chat_id = message.chat.id
    user_info = message.from_user
    selected_api = user_state[chat_id]
    query_text = message.text
    
    if query_text in APIS:
        handle_menu_click(message)
        return

    try:
        bot.send_message(ADMIN_ID, f"📢 **Log:** {user_info.first_name}\n🛠 **Tool:** {selected_api}\n📝 **Query:** `{query_text}`")
    except: pass

    wait_msg = bot.send_message(chat_id, "⏳ Raw Data fetch ho raha hai...")
    del user_state[chat_id]

    try:
        url = APIS[selected_api].format(query_text)
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        try:
            raw_data = response.json()
            pretty_json = json.dumps(raw_data, indent=2, ensure_ascii=False)
            
            header = f"✅ **Result for {selected_api}:**\n"
            full_response = f"{header}```json\n{pretty_json}\n```\n{DEV_TAG}"
            
            bot.delete_message(chat_id, wait_msg.message_id)
            send_long_message(chat_id, full_response)
            
        except:
            bot.edit_message_text(f"⚠️ **Response:**\n`{response.text[:1000]}`\n{DEV_TAG}", chat_id, wait_msg.message_id)
            
    except:
        bot.edit_message_text(f"❌ Error: API ne response nahi diya!{DEV_TAG}", chat_id, wait_msg.message_id)

if __name__ == "__main__":
    bot.remove_webhook()
    print("H4CKERR MX Bot Ready!")
    bot.infinity_polling()
