from flask import Flask
import threading
import telebot
import sqlite3
import urllib.request
import json

# 🌐 Flask መተግበሪያ ለ Render ፖርት ማስተካከያ
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Flaskን በሌላ Thread ማስነሳት (Render ፖርት እንዳያጣ)
threading.Thread(target=run_flask).start()

# 🔑 የአንተ አዲሱ የተስተካከለው ቦት ቶከን እዚህ ገብቷል
BOT_TOKEN = "8843208104:AAHtRuqwviHgvN8xFtH54hpUtM2fsuFfAN0"
YOUTUBE_API_KEY = "AIzaSyBlQndpoOcFywClxG5OyW2245efMEBWk1k"
YOUTUBE_CHANNEL_ID = "UCD9fsC6ueA2rrbh5ceMBMsA"

# 👑 የአንተ የቴሌግራም ID
ADMIN_ID = 7547455364  

bot = telebot.TeleBot(BOT_TOKEN)

# 👥 የኅብረቱ ልጆች ዝርዝር
HIBRET_MEMBERS = [6855238181, 7744855538, 7466483442]  

# የዳታቤዝ ግንኙነት
conn = sqlite3.connect("challenge.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        referred_by INTEGER,
        points INTEGER DEFAULT 0,
        is_verified INTEGER DEFAULT 0
    )
""")
conn.commit()

def check_youtube_subscription(user_youtube_channel_url):
    try:
        if "/channel/" in user_youtube_channel_url:
            user_channel_id = user_youtube_channel_url.split("/channel/")[-1].split("/")[0]
        elif "@" in user_youtube_channel_url:
            user_channel_id = user_youtube_channel_url.split("@")[-1].split("/")[0]
        else:
            return False
        
        url = f"https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&channelId={user_channel_id}&forChannelId={YOUTUBE_CHANNEL_ID}&key={YOUTUBE_API_KEY}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if "items" in data and len(data["items"]) > 0:
                return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

@bot.message_handler(commands=["start"])
def start_command(message):
    user_id = message.from_user.id
    text_parts = message.text.split()
    
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_exists = cursor.fetchone()
    
    if not user_exists:
        referred_by = int(text_parts[1]) if len(text_parts) > 1 and text_parts[1].isdigit() else None
        cursor.execute("INSERT INTO users (user_id, referred_by) VALUES (?, ?)", (user_id, referred_by))
        conn.commit()
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_link = telebot.types.KeyboardButton("🔗 የእኔ መወዳደሪያ ሊንክ")
    btn_status = telebot.types.KeyboardButton("📊 የእኔ ነጥብ")
    markup.add(btn_link, btn_status)
    
    if user_id in HIBRET_MEMBERS:
        hibret_text = (
            "👋 ሰላም! ወደ ሳበህ ሚዲያ የውድድር ማስተዳደሪያ ቦት እንኳን መጡ。\n\n"
            "እርስዎ የኅብረቱ ተወዳዳሪ አባል ነዎት። ከታች ያሉትን ቁልፎች በመጠቀም ልዩ የመወዳደሪያ ሊንክዎን ማውጣት Blunt "
            "ሰዎችን መጋበዝ እና ከፍተኛ ነጥብ በመሰብሰብ የውድድሩ ማጠቃለያ ላይ የሚሰጠውን ትልቅ ሽልማት ማሸነፍ ይችላሉ! 🏆"
        )
        bot.reply_to(message, hibret_text, reply_markup=markup)
    else:
        guest_text = (
            f"👋 ሰላም! ወደ ሳበህ ሚዲያ የሽልማት ውድድር ቦት እንኳን መጡ。\n\n"
            f"ይህ ከፍተኛ ነጥብ ላስመዘገቡ ተወዳዳሪዎች የሚያማምሩ ሽልማቶች የሚሰጥበት ልዩ ውድድር ነው! 🏆\n\n"
            f"ውድድሩን ለመቀላቀል እና ጋባዥዎን ለመርዳት መጀመሪያ የዩቲዩብ ቻናላችንን Subscribe ያድርጉ。\n"
            f"ሊንክ፦ https://youtube.com/channel/{YOUTUBE_CHANNEL_ID}\n\n"
            f"ከዚያ ሰብስክራይብ ያደረጉበትን የራስዎን የዩቲዩብ ቻናል ሊንክ (Channel URL) በጽሑፍ እዚህ ይላኩ..."
        )
        bot.reply_to(message, guest_text, reply_markup=markup)

@bot.message_handler(commands=["admin_panel"])
def admin_panel_command(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        cursor.execute("SELECT user_id, points FROM users WHERE user_id IN ({}) ORDER BY points DESC".format(",".join(["?"]*len(HIBRET_MEMBERS))), HIBRET_MEMBERS)
        results = cursor.fetchall()
        
        report_text = "🏆 **የተወዳዳሪዎች ወቅታዊ የነጥብ ደረጃ** 🏆\n\n"
        for index, row in enumerate(results, start=1):
            report_text += f"{index}. ተወዳዳሪ ID: `{row[0]}` -> 📊 **{row[1]} ነጥብ**\n"
            
        bot.reply_to(message, report_text, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ ይቅርታ! ይህ ማዘዣ ለዋናው አድሚን ብቻ የተፈቀደ ነው።")

@bot.message_handler(func=lambda message: message.text in ["🔗 የእኔ መወዳደሪያ ሊንክ", "📊 የእኔ ነጥብ"])
def buttons_handler(message):
    user_id = message.from_user.id
    
    if message.text == "🔗 የእኔ መወዳደሪያ ሊንክ":
        if user_id in HIBRET_MEMBERS:
            bot_username = bot.get_me().username
            referral_link = f"https://t.me/{bot_username}?start={user_id}"
            
            msg_text = (
                f"👋 ሰላም ጓደኞቼ! እባካችሁ በትልቅ ትብብር ይህንን ሊንክ ተጭናችሁ ውድድሩን ተቀላቀሉልኝ! 🙏\n\n"
                f"እኔ በሳበህ የሽልማት ውድድር ላይ እየተሳተፍኩኝ ነው፤ የውድድሩ ማጠቃለያ ላይ ከፍተኛ ነጥብ ላመጣ ትልቅ ሽልማት ይበረከታል! 🏆 "
                f"እናንተ ሊንኩን ተጭናችሁ ቦቱን ስትጀምሩ እና ቻናሉን Subscribe ስታደርጉ ለእኔ 1 ነጥብ ይቆጠርልኛል፤ አሸናፊ እንድሆን ትልቅ እገዛ ይሆንኛል! ✨\n\n"
                f"የመወዳደሪያ ሊንኬ ይሄ ነው 👇\n{referral_link}"
            )
            bot.reply_to(message, msg_text)
        else:
            bot.reply_to(message, "❌ ይቅርታ! እርስዎ የኅብረቱ አባል ስላልሆኑ የመወዳደሪያ ሊንክ ማውጣት አይችሉም... ")
            
    elif message.text == "📊 የእኔ ነጥብ":
        cursor.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
        res = cursor.fetchone()
        points = res[0] if res else 0
        bot.reply_to(message, f"📊 በአሁኑ ሰዓት ያለዎት አጠቃላይ ነጥብ፡ {points} ነጥብ ነው። በርቱና ተጨማሪ ነጥብ በመሰብሰብ የሽልማቱ ባለቤት ይሁኑ! 🔥")

@bot.message_handler(func=lambda message: "youtube.com/" in message.text)
def handle_youtube_link(message):
    user_id = message.from_user.id
    user_link = message.text
    
    cursor.execute("SELECT is_verified, referred_by FROM users WHERE user_id = ?", (user_id,))
    res = cursor.fetchone()
    
    if res and res[0] == 1:
        bot.reply_to(message, "✅ የእርስዎ አካውንት አስቀድሞ ተረጋግጧል!")
        return
        
    bot.reply_to(message, "🔄 የሰብስክራይብ ሁኔታዎን በራስ-ሰር እያረጋገጥኩ ነው፣ እባክዎ ጥቂት ሰከንዶች ይጠብቁ...")
    
    if check_youtube_subscription(user_link):
        referred_by = res[1] if res else None
        cursor.execute("UPDATE users SET is_verified = 1 WHERE user_id = ?", (user_id,))
        
        if referred_by and (referred_by in HIBRET_MEMBERS):
            cursor.execute("UPDATE users SET points = points + 1 WHERE user_id = ?", (referred_by,))
            try:
                bot.send_message(referred_by, "🎉 እንኳን ደስ አለዎት! በአዲስ ሰው ግብዣ 1 ነጥብ ተጨምሮልዎታል። ወደ ሽልማቱ አንድ እርምጃ ተቃርበዋል!")
            except:
                pass
                
        conn.commit()
        bot.reply_to(message, "🎉 ድንቅ ነው! ሰብስክራይብ ማድረጎ በሲስተማችን ተረጋግጧል። ለጋባዥዎ 1 ነጥብ ተቆጥሮለታል። ለተሳትፎዎ እናመሰግናለን!")
    else:
        bot.reply_to(message, "❌ ይቅርታ፣ ያቀረቡት አካውንት ቻናላችንን Subscribe ማድረጉ አልተረጋገጠም። እባክዎ መጀመሪያ ሰብስክራይብ ማድረጎን እና የዩቲዩብ አካውንቶ 'Public' (ለሁሉም ክፍት) መሆኑን ያረጋግጡ...")

if __name__ == "__main__":
    print("🤖 ቦቱ በተሳካ ሁኔታ ሥራ ጀምሯል...")
    bot.polling(none_stop=True, timeout=60)

