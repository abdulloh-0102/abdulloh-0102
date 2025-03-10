import os
import telebot
import speech_recognition as sr
from pydub import AudioSegment

# Bot tokenini shu yerga kiriting
BOT_TOKEN = "7581089872:AAFnnCuctZdaN4w3XXpb3ItNMjT4WS6a4AA"

# Botni yaratamiz
bot = telebot.TeleBot(BOT_TOKEN)

# Ovozli xabarni matnga o‘girish funksiyasi
def ovozni_matnga(audio_fayl):
    tanib_olish = sr.Recognizer()

    # Faylni WAV formatiga o‘tkazish
    if not audio_fayl.endswith(".wav"):
        ovoz = AudioSegment.from_file(audio_fayl)
        audio_fayl = "temp_audio.wav"
        ovoz.export(audio_fayl, format="wav")

    with sr.AudioFile(audio_fayl) as manba:
        audio = tanib_olish.record(manba)

    try:
        matn = tanib_olish.recognize_google(audio, language='uz-UZ')
        return matn
    except sr.UnknownValueError:
        return "❌ Ovoz tushunilmadi. Iltimos, aniqroq gapiring!"
    except sr.RequestError:
        return "⚠️ Xatolik yuz berdi. Internet aloqasini tekshiring."

# /start buyrug‘iga javob
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "🤖 Assalomu alaykum! Men ovozni matnga o‘girish botiman. \n🎤 Iltimos, audio yoki ovozli xabar yuboring!")

# Voice message qabul qilish
@bot.message_handler(content_types=['voice'])
def ovozli_xabar(message):
    bot.send_message(message.chat.id, "🔄 Ovozli xabar qayta ishlanmoqda...")
    
    # Telegramdan faylni yuklab olish
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Faylni saqlash
    file_path = "downloads/voice.ogg"
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Ovozni matnga o‘girish
    matn = ovozni_matnga(file_path)

    # Foydalanuvchiga javob yuborish
    bot.send_message(message.chat.id, f"📜 *Matn:* {matn}", parse_mode="Markdown")

    # Faylni o‘chirish
    os.remove(file_path)

# Audio fayllarni qabul qilish
@bot.message_handler(content_types=['audio', 'document'])
def audio_qabul(message):
    bot.send_message(message.chat.id, "🔄 Audio fayl qayta ishlanmoqda...")

    # Telegramdan faylni yuklab olish
    file_info = bot.get_file(message.audio.file_id if message.audio else message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Fayl turi
    file_format = message.audio.mime_type.split('/')[-1] if message.audio else message.document.mime_type.split('/')[-1]
    file_path = f"downloads/audio.{file_format}"

    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Ovozni matnga o‘girish
    matn = ovozni_matnga(file_path)

    # Foydalanuvchiga javob yuborish
    bot.send_message(message.chat.id, f"📜 *Matn:* {matn}", parse_mode="Markdown")

    # Faylni o‘chirish
    os.remove(file_path)

# Botni ishga tushirish
if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    bot.infinity_polling()
