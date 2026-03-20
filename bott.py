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

# --- ALL APIS (Merged & Updated) ---
APIS = {
    # --- H4CKERR MX SPECIAL ---
    "🔍 GST Lookup": "https://paid.proportalxc.workers.dev/gst?gst={}",
    "📍 Pincode Search": "https://paid.proportalxc.workers.dev/pincode?pincode={}",
    "🌐 IP Detail": "https://paid.proportalxc.workers.dev/ip?ip={}",
    
    # --- OSINT LOOKUPS ---
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
    "💳 BIN Lookup": "https://lookup.binlist.net/{}",
    
    # --- FREE FIRE APIS (Server: 203.57.85.58:2005) ---
    "🎮 FF Player Info": "http://203.57.85.58:2005/player-info?uid={}",
    "🚫 FF Ban Check": "http://203.57.85.58:2005/bancheck?uid={}",
    "📊 FF Level Check": "http://203.57.85.58:2005/level?uid={}",
    "🌍 FF Region": "http://203.57.85.58:2005/region?uid={}",
    "🎁 FF Wishlist": "http://203.57.85.58:2005/wishlist?uid={}",
    "🔍 FF Name Search": "http://203.57.85.58:2005/search?name={}",
    "🎫 FF Token Decode": "http://203.57.85.58:2005/decode?token={}",
    "📅 FF Events": "http://203.57.85.58:2005/events?region={}"
}

# --- EXAMPLES FOR ALL ---
EXAMPLES = {
    # H4CKERR MX
    "🔍 GST Lookup": "Example: `07AAAAA0000A1Z5` (Enter 15-digit GSTIN)",
    "📍 Pincode Search": "Example: `110001` (Enter 6-digit Area Pincode)",
    "🌐 IP Detail": "Example: `8.8.8.8` (Enter IPv4 Address)",
    
    # OSINT
    "📱 Phone Lookup": "Example: `91XXXXXXXXXX` (Mobile with Country Code)",
    "📍 Num Trace": "Example: `92XXXXXXXXXX` (International format)",
    "🇵🇰 Pak Phone": "Example: `03XXXXXXXXX` (Pakistan Mobile Number)",
    "🆔 Aadhaar Lookup": "Example: `Rajesh Kumar` (Enter Full Name)",
    "👥 Family Info": "Example: `91XXXXXXXXXX` (Target Mobile Number)",
    "👤 Num Owner": "Example: `91XXXXXXXXXX` (Search Name by Number)",
    "🚗 Vehicle Num": "Example: `DL10CE1234` (Enter RC Number)",
    "📧 Email Lookup": "Example: `user@gmail.com` (Enter Email Address)",
    "🐙 GitHub Profile": "Example: `torvalds` (Enter GitHub Username)",
    "🔍 Domain/Whois": "Example: `google.com` (Enter Domain Name)",
    "🏦 IFSC Lookup": "Example: `SBIN0001234` (Enter Bank IFSC Code)",
    "💳 BIN Lookup": "Example: `457173` (First 6 digits of Card)",
    
    # FREE FIRE
    "🎮 FF Player Info": "Example: `2919267964` (Numeric Player UID)",
    "🚫 FF Ban Check": "Example: `2919267964` (Numeric Player UID)",
    "📊 FF Level Check": "Example: `2919267964` (Numeric Player UID)",
    "🌍 FF Region": "Example: `2919267964` (Numeric Player UID)",
    "🎁 FF Wishlist": "Example: `2919267964` (Numeric Player UID)",
    "🔍 FF Name Search": "Example: `yash` (Player In-game Name)",
    "🎫 FF Token Decode": "Example: `eyJhbGci...` (Paste the Full JWT Token)",
    "📅 FF Events": "Example: `europe` or `indonesia` (Region Name)"
}

user_state = {}
DEV_TAG = "\n\n━━━━━━━━━━━━━━━\n👤 **Developer:- @hackerrmx69**"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(name) for name in APIS.keys()]
    markup.add(*buttons)
    bot.send_message(
        message.chat.id, 
        "💀 **H4CKERR MX Multi-Lookup Bot Ready!**\n\nAb tak ki sabse advanced APIs set hain 👇", 
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
    
    # If user clicks another button instead of typing
    if query_text in APIS:
        handle_menu_click(message)
        return

    # Admin Logging
    try:
        log = f"📢 **H4CKERR MX Log**\n👤 **User:** {user_info.first_name} (@{user_info.username})\n🛠 **Tool:** {selected_api}\n📝 **Query:** `{query_text}`"
        bot.send_message(ADMIN_ID, log, parse_mode='Markdown')
    except: pass

    wait_msg = bot.send_message(chat_id, "⏳ Fetching Premium Data (H4CKERR MX Server)...")
    del user_state[chat_id]

    try:
        url = APIS[selected_api].format(query_text)
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        try:
            raw_data = response.json()
            pretty_json = json.dumps(raw_data, indent=2, ensure_ascii=False)
            
            if len(pretty_json) > 3800:
                filename = f"h4ckerr_{chat_id}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(pretty_json)
                bot.send_document(chat_id, open(filename, "rb"), caption=f"📄 Result: {selected_api}{DEV_TAG}", parse_mode='Markdown')
                bot.delete_message(chat_id, wait_msg.message_id)
                os.remove(filename)
            else:
                bot.edit_message_text(f"✅ **Result:**\n```json\n{pretty_json}\n```\n{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')
        except:
            bot.edit_message_text(f"⚠️ **Response:** `{response.text[:1000]}`{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')
            
    except:
        bot.edit_message_text(f"❌ Error: API Down hai ya request block ho gayi!{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    bot.remove_webhook()
    print("H4CKERR MX Bot is LIVE!")
    bot.infinity_polling()
