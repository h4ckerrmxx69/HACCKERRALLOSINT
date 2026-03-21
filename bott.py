import telebot
import requests
import json
import os
import time
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = "8411017661:AAFYSg_0ATzf-sPmoj-it77t3pp_4RAyWUg"
ADMIN_ID = 5192884021  # <--- Apni ID check kar lena
bot = telebot.TeleBot(API_TOKEN)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- ALL APIS ---
APIS = {
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "👤 Num Owner": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🆔 Aadhaar Lookup": "https://aadhar.ek4nsh.in/?name={}",
    "📸 Insta Lookup": "https://allnew.proportalxc.workers.dev/instagram?username={}",
    "🔍 GST Lookup": "https://paid.proportalxc.workers.dev/gst?gst={}",
    "📍 Pincode Search": "https://paid.proportalxc.workers.dev/pincode?pincode={}",
    "🌐 IP Detail": "https://paid.proportalxc.workers.dev/ip?ip={}",
    "🚗 Vehicle V2": "https://api.b77bf911.workers.dev/v2?query={}",
    "💳 PAN Lookup": "https://api.b77bf911.workers.dev/pan?user={}",
    "🌾 Rashan Card": "https://api.b77bf911.workers.dev/rashan?aadhaar={}",
    "💸 UPI Lookup": "https://api.b77bf911.workers.dev/upi?user={}",
    "📡 Telegram Info": "https://api.b77bf911.workers.dev/telegram?user={}",
    "🎮 FF Player Info": "http://203.57.85.58:2005/player-info?uid={}&key=@yashapis",
    "🚫 FF Ban Check": "http://203.57.85.58:2005/bancheck?uid={}&key=@yashapis",
    "📊 FF Level Check": "http://203.57.85.58:2005/level?uid={}&key=@yashapis",
    "🎫 FF Token Decode": "http://203.57.85.58:2005/decode?token={}&key=@yashapis",
    "🔍 Domain/Whois": "https://api.hackertarget.com/whois/?q={}"
}

# --- ALL EXAMPLES ---
EXAMPLES = {
    "📱 Phone Lookup": "Example: `91XXXXXXXXXX` (With Country Code)",
    "🆔 Aadhaar Lookup": "Example: `Rajesh Kumar` (Full Name)",
    "🎮 FF Player Info": "Example: `2919267964` (UID)",
    "📸 Insta Lookup": "Example: `physicswallah` (Username)"
}

user_state = {}
DEV_TAG = "\n\n━━━━━━━━━━━━━━━\n👤 **Developer:- @hackerrmx69**"

def send_long_message(chat_id, text):
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
    bot.send_message(message.chat.id, "💀 **H4CKERR MX V18.0**\nSaare logs aur data check fixed! 👇", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in APIS.keys())
def handle_menu_click(message):
    user_state[message.chat.id] = message.text
    instruction = EXAMPLES.get(message.text, "Apni query enter karein:")
    bot.send_message(message.chat.id, f"🛠 **Tool:** {message.text}\n📝 **Instruction:** {instruction}", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def process_lookup(message):
    chat_id = message.chat.id
    user = message.from_user
    selected_api = user_state[chat_id]
    query = message.text
    
    if query in APIS:
        handle_menu_click(message)
        return

    # --- FULL ADMIN LOG (Username + ID + Name) ---
    try:
        username = f"@{user.username}" if user.username else "None"
        log_text = (
            "📢 **New Request Log**\n"
            f"👤 **Name:** {user.first_name}\n"
            f"🆔 **User ID:** `{user.id}`\n"
            f"🔗 **Username:** {username}\n"
            f"🛠 **Tool:** {selected_api}\n"
            f"📝 **Query:** `{query}`"
        )
        bot.send_message(ADMIN_ID, log_text, parse_mode='Markdown')
    except: pass

    wait = bot.send_message(chat_id, "⏳ Searching in database...")
    del user_state[chat_id]

    try:
        url = APIS[selected_api].format(query)
        res = requests.get(url, headers=HEADERS, timeout=12)
        
        try:
            data = res.json()
            
            # Agar results khali hain (Jo tera error tha)
            if "results" in data and not data["results"] and data.get("count") == 0:
                bot.edit_message_text(f"❌ **No Data Found!**\nServer ke database mein iss query ka koi record nahi mila.{DEV_TAG}", chat_id, wait.message_id, parse_mode='Markdown')
                return

            pretty = json.dumps(data, indent=2, ensure_ascii=False)
            bot.delete_message(chat_id, wait.message_id)
            send_long_message(chat_id, f"✅ **Result ({selected_api}):**\n```json\n{pretty}\n```\n{DEV_TAG}")
        except:
            bot.edit_message_text(f"⚠️ **Server Response:**\n`{res.text[:1000]}`{DEV_TAG}", chat_id, wait.message_id, parse_mode='Markdown')
    except:
        bot.edit_message_text(f"❌ Error: API Down hai ya respond nahi kar rahi!{DEV_TAG}", chat_id, wait.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
    
