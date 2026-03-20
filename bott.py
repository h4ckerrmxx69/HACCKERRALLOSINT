import telebot
import requests
import json
import os
import time
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = "8411017661:AAFYSg_0ATzf-sPmoj-it77t3pp_4RAyWUg"
ADMIN_ID = 5192884021  # <--- Yahan apni numerical Telegram ID daalein
bot = telebot.TeleBot(API_TOKEN)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- ALL APIS (Parameter Fix: ?user= for Workers) ---
APIS = {
    # --- H4CKERR MX SPECIAL ---
    "📸 Insta Lookup": "https://allnew.proportalxc.workers.dev/instagram?username={}",
    "🔍 GST Lookup": "https://paid.proportalxc.workers.dev/gst?gst={}",
    "📍 Pincode Search": "https://paid.proportalxc.workers.dev/pincode?pincode={}",
    "🌐 IP Detail": "https://paid.proportalxc.workers.dev/ip?ip={}",
    
    # --- FIXED WORKER ENDPOINTS (Missing Parameter Fix) ---
    "💳 PAN Lookup": "https://api.b77bf911.workers.dev/pan?user={}",
    "🌾 Rashan Card": "https://api.b77bf911.workers.dev/rashan?user={}",
    "💸 UPI Lookup": "https://api.b77bf911.workers.dev/upi?user={}",
    "🏦 UPI V2": "https://api.b77bf911.workers.dev/upi2?user={}",
    "🚗 Vehicle V2": "https://api.b77bf911.workers.dev/v2?user={}",
    "📡 Telegram Info": "https://api.b77bf911.workers.dev/telegram?user={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?user={}",
    
    # --- FREE FIRE NEW SERVER (203.57.85.58:2005) ---
    "🎮 FF Player Info": "http://203.57.85.58:2005/player-info?uid={}",
    "🚫 FF Ban Check": "http://203.57.85.58:2005/bancheck?uid={}",
    "📊 FF Level Check": "http://203.57.85.58:2005/level?uid={}",
    "🌍 FF Region": "http://203.57.85.58:2005/region?uid={}",
    "🎁 FF Wishlist": "http://203.57.85.58:2005/wishlist?uid={}",
    "🔍 FF Name Search": "http://203.57.85.58:2005/search?name={}",
    "🎫 FF Token Decode": "http://203.57.85.58:2005/decode?token={}",

    # --- OSINT & UTILITY ---
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "📍 Num Trace": "https://ab-calltraceapi.vercel.app/info?number={}",
    "🇵🇰 Pak Phone": "https://abbas-apis.vercel.app/api/pakistan?number={}",
    "🆔 Aadhaar Lookup": "https://aadhar.ek4nsh.in/?name={}",
    "👤 Num Owner": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🚗 Vehicle Num": "https://new-vehicle-api-eosin.vercel.app/vehicle?rc={}",
    "📧 Email Lookup": "https://api.eva.pingutil.com/email?email={}",
    "🐙 GitHub Profile": "https://abbas-apis.vercel.app/api/github?username={}",
    "🔍 Domain/Whois": "https://api.hackertarget.com/whois/?q={}",
    "💳 BIN Lookup": "https://lookup.binlist.net/{}"
}

# --- COMPLETE EXAMPLES FOR ALL ---
EXAMPLES = {
    "📸 Insta Lookup": "Example: `physicswallah` (Username)",
    "🔍 GST Lookup": "Example: `07AAAAA0000A1Z5` (GSTIN)",
    "📍 Pincode Search": "Example: `110001` (6-digit Pin)",
    "🌐 IP Detail": "Example: `8.8.8.8` (IPv4 Address)",
    "💳 PAN Lookup": "Example: `ABCDE1234F` (PAN Number)",
    "🌾 Rashan Card": "Example: `123456789012` (Rashan ID)",
    "💸 UPI Lookup": "Example: `paytm@upi` (UPI ID)",
    "📡 Telegram Info": "Example: `12345678` (Telegram UID)",
    "🚗 Vehicle V2": "Example: `DL10CE1234` (RC No)",
    "🎮 FF Player Info": "Example: `2919267964` (Numeric UID)",
    "🚫 FF Ban Check": "Example: `2919267964` (Numeric UID)",
    "🔍 FF Name Search": "Example: `yash` (In-game Name)",
    "📱 Phone Lookup": "Example: `91XXXXXXXXXX` (With Country Code)",
    "🆔 Aadhaar Lookup": "Example: `Rajesh Kumar` (Full Name)",
    "📧 Email Lookup": "Example: `test@gmail.com` (Email Address)",
    "🔍 Domain/Whois": "Example: `google.com` (Domain Name)",
    "🏦 IFSC Lookup": "Example: `SBIN0001234` (IFSC Code)"
}

user_state = {}
DEV_TAG = "\n\n━━━━━━━━━━━━━━━\n👤 **Developer:- @hackerrmx69**"

def send_long_message(chat_id, text):
    """Chunking system for long JSON data"""
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
        "💀 **H4CKERR MX Ultimate V8.0**\n\nAll Endpoints Fixed! Choose a tool 👇", 
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
        f"🛠 **Selected:** {service}\n📝 **Instruction:** {instruction}", 
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
        log = f"📢 **H4CKERR MX Log**\n👤 **User:** {user_info.first_name} (@{user_info.username})\n🛠 **Tool:** {selected_api}\n📝 **Query:** `{query_text}`"
        bot.send_message(ADMIN_ID, log)
    except: pass

    wait_msg = bot.send_message(chat_id, f"⏳ Fetching Full Data for {selected_api}...")
    del user_state[chat_id]

    try:
        url = APIS[selected_api].format(query_text)
        response = requests.get(url, headers=HEADERS, timeout=20)
        
        try:
            raw_data = response.json()
            pretty_json = json.dumps(raw_data, indent=2, ensure_ascii=False)
            
            header = f"✅ **Raw JSON Result ({selected_api}):**\n"
            full_response = f"{header}```json\n{pretty_json}\n```\n{DEV_TAG}"
            
            bot.delete_message(chat_id, wait_msg.message_id)
            send_long_message(chat_id, full_response)
            
        except:
            bot.edit_message_text(f"⚠️ **Response:**\n`{response.text[:1000]}`\n{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')
            
    except Exception as e:
        bot.edit_message_text(f"❌ Error: Server connection failed!{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    print("H4CKERR MX V8.0 is LIVE!")
    bot.remove_webhook()
    bot.infinity_polling()
