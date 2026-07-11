import telebot
from telebot import types

TOKEN = '8537661220:AAFPA-12-BLYmt5XWwlkBi624XWYh-wLZgY'
bot = telebot.TeleBot(TOKEN)

# --- ዳታቤዝ ---

bible_data = {
    "📌 ስለ ቤዛነት": "ክርስቶስ እኛን ለማዳን ሲል ሰው ሆነ፣ መከራን ተቀበለ፣ ሞተ፣ በሦስተኛውም ቀን ተነሳ። (1ኛ ጴጥ 2:24)",
    "📌 ስለ ምሥጢረ ሥጋዌ": "ቃል ሥጋ ሆነ (ዮሐ 1:14)። ይህም ማለት መለኮትና ትስብእት ያለ መለወጥና ያለ መቀላቀል አንድ አካል አንድ ባሕርይ ሆኑ ማለት ነው።",
    "📌 ስለ ክርስቶስ አምላክነት": "ክርስቶስ ፍጹም አምላክ ፍጹም ሰው ነው። (ሮሜ 9:5)"
}

trinity_qa = {
    "❓ ሦስትነትና አንድነት": "ሥላሴ በባሕርይ፣ በሕልውና፣ በፈቃድና በመለኮት <b>አንድ</b> ናቸው። በስም፣ በአካልና በግብር <b>ሦስት</b> ናቸው።",
    "❓ የሥላሴ ምሳሌዎች": "<b>ፀሐይ፦</b> ክበቧ የአብ፣ ብርሃኗ የወልድ፣ ሙቀቷ የመንፈስ ቅዱስ ምሳሌ ነው።"
}

# አዳዲስ የስህተት ትምህርቶች እዚህ ተጨምረዋል
councils_data = {
    "🔹 የኒቂያ ጉባኤ": "<b>325 ዓ.ም፦</b> በአርዮስ ላይ የተደረገ። ወልድ ከአብ ጋር በባሕርይ አንድ መሆኑ ተረጋገጠ።",
    "🔹 የቁስጥንጥንያ": "<b>381 ዓ.ም፦</b> በመቅዶንዮስ ላይ የተደረገ። መንፈስ ቅዱስ አምላክ መሆኑ ተረጋገጠ።",
    "🔹 የኤፌሶን ጉባኤ": "<b>431 ዓ.ም፦</b> በንስጥሮስ ላይ የተደረገ። ድንግል ማርያም 'የአምላክ እናት' መሆኗ ተረጋገጠ።",
    "⚠️ ዶሴቲዝም (Docetism)": "<b>ትምህርቱ፦</b> 'ክርስቶስ እውነተኛ ሥጋ አልነበረውም፤ እንደ ጥላ ወይም እንደ ምትሃት ነው የታየው' የሚል ጥንታዊ ስህተት ነው። <b>ምላሽ፦</b> ሐዋርያው ቅዱስ ዮሐንስ 'ኢየሱስ ክርስቶስ በሥጋ እንደ መጣ የማይታመን መንፈስ ሁሉ ከእግዚአብሔር አይደለም' በማለት ጥርቅም አድርጎ መልሶታል። (1ኛ ዮሐ 4:2-3)",
    "⚠️ ግኖስቲሲዝም (Gnosticism)": "<b>ትምህርቱ፦</b> 'ድኅነት የሚገኘው በዕውቀት (Gnosis) ብቻ ነው፤ ሥጋ ደግሞ ክፉ ነው' የሚሉ ነበሩ። <b>ምላሽ፦</b> ቤተክርስቲያን ድኅነት በክርስቶስ ቤዛነትና በእምነት መሆኑን፣ ሥጋም የእግዚአብሔር ፍጥረት መሆኑን አስተምራለች።",
    "⚠️ የአርዮስ ስሕተት": "<b>ትምህርቱ፦</b> 'ወልድ ፍጡር ነው' የሚል። <b>ምላሽ፦</b> በኒቂያ ጉባኤ ተወግዟል።",
    "⚠️ የንስጥሮስ ስሕተት": "<b>ትምህርቱ፦</b> 'ማርያም የሰውን እናት እንጂ የአምላክ እናት አትባልም' የሚል። <b>ምላሽ፦</b> በኤፌሶን ተወግዟል።"
}

advice_data = {
    "✨ ስለ ትሕትና": "<b>ቅዱስ ይስሐቅ፦</b> 'ትሕትና የክርስቶስ ልብስ ነው።'",
    "✨ ስለ ፍቅር": "<b>ቅዱስ ዮሐንስ አፈወርቅ፦</b> 'ፍቅር የሌለው ሃይማኖት እንደሌለ እወቅ።'"
}

# --- ሜኑ አደራጃጀት ---

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("📖 ከመጽሐፍ ቅዱስ", "☀️ ትምህርተ ሥላሴ", "📜 የጉባኤያት ታሪክ", "💡 የአባቶች ምክር")
    bot.send_message(message.chat.id, "እንኳን ወደ Patristic Wisdom መጡ። ርዕስ ይምረጡ፡", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    cid = message.chat.id
    txt = message.text

    def send_submenu(data_dict, prompt_text):
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for key in data_dict.keys(): markup.add(types.KeyboardButton(key))
        markup.add("🔙 ወደ ዋናው ማውጫ")
        bot.send_message(cid, prompt_text, reply_markup=markup)

    if txt == "📖 ከመጽሐፍ ቅዱስ": send_submenu(bible_data, "የመጽሐፍ ቅዱስ ትርጓሜ ንዑስ ርዕሶች፡")
    elif txt == "☀️ ትምህርተ ሥላሴ": send_submenu(trinity_qa, "ስለ ሥላሴ ዝርዝር ጥያቄዎች፡")
    elif txt == "📜 የጉባኤያት ታሪክ": send_submenu(councils_data, "የጉባኤያት ታሪክና የስሕተት ትምህርቶች (መናፍቃን)፡")
    elif txt == "💡 የአባቶች ምክር": send_submenu(advice_data, "የአባቶች መንፈሳዊ ምክሮች፡")

    elif txt in bible_data: bot.send_message(cid, bible_data[txt], parse_mode="HTML")
    elif txt in trinity_qa: bot.send_message(cid, trinity_qa[txt], parse_mode="HTML")
    elif txt in advice_data: bot.send_message(cid, advice_data[txt], parse_mode="HTML")
    elif txt in councils_data: bot.send_message(cid, councils_data[txt], parse_mode="HTML")

    elif txt == "🔙 ወደ ዋናው ማውጫ": start(message)

print("ቦቱ ስራ ጀምሯል...")
bot.polling()
