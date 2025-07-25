import os
import schedule
import threading
import time
from datetime import datetime, timedelta
import pytz
import telebot
from telebot import types
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

# Flask для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Phuket Beach Bot is running! 🏖️"

@app.route('/health')
def health():
    return "OK", 200

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# Ваши chat_id для автопостинга
CHAT_ID = os.environ.get('CHAT_ID')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

# Временная зона Пхукета
TIMEZONE = pytz.timezone('Asia/Bangkok')

# Функция для отправки в чат и канал
def send_to_all(text):
    """Отправляет сообщение в чат и канал"""
    try:
        if CHAT_ID:
            bot.send_message(CHAT_ID, text, parse_mode='Markdown', disable_web_page_preview=True)
        if CHANNEL_ID:
            bot.send_message(CHANNEL_ID, text, parse_mode='Markdown', disable_web_page_preview=True)
        print(f"✅ Автопостинг в {datetime.now(TIMEZONE).strftime('%H:%M')}")
    except Exception as e:
        print(f"❌ Ошибка автопостинга: {e}")

# Генерация утренней сводки
def get_morning_report():
    current_time = datetime.now(TIMEZONE).strftime('%d.%m.%Y')
    
    return f"""
🏝️ *Доброе утро! Пляжи Пхукета - {current_time}*

🏖️ *Общие условия:*
🌗 Фаза Луны: Убывающая
🌊 Приливы: 05:18, 18:42
🏖️ Отливы: 11:09, 23:20
🌡 Температура воды: 29.2°C
🌬 Ветер: 13 км/ч СВ
🌊 Волны: 0.9 м
☁️ Погода: Переменная облачность
🌡 Воздух: 28°C

🚩 *Флаги на пляжах:*
• Патонг: 🟢 Зеленый
• Карон: 🟢 Зеленый
• Ката: 🟡 Желтый
• Камала: 🟢 Зеленый

🏊‍♂️ *Купание:* Безопасно!
🪼 *Медузы:* Не замечены
🐢 *Черепахи:* Активны у Май Кхао

💫 *Совет дня:* Лучшие пляжи сегодня - Ката Ной и Най Харн
    """

# Генерация дневного обновления
def get_noon_update():
    return f"""
☀️ *Дневное обновление - {datetime.now(TIMEZONE).strftime('%H:%M')}*

🌊 *Актуальные условия:*
🌡 Вода: 29.8°C
🌬 Ветер: 18 км/ч
🌊 Волны: 1.1 м
☁️ Погода: Малооблачно
🌡 Воздух: 34°C

⚠️ *УФ-ПРЕДУПРЕЖДЕНИЕ:*
☀️ УФ-индекс: 11 (ЭКСТРЕМАЛЬНЫЙ!)
🧴 Используйте крем SPF 50+
⏰ Ограничьте пребывание на солнце

⛵ *Для яхтсменов:*
Ветер усилился - умеренная качка

🐢 *Природа:* Черепахи замечены у северных скал!
    """

# Генерация вечернего отчета
def get_evening_update():
    sunset_time = datetime.now(TIMEZONE).replace(hour=18, minute=47)
    now = datetime.now(TIMEZONE)
    time_to_sunset = sunset_time - now
    hours = int(time_to_sunset.seconds / 3600) if time_to_sunset.total_seconds() > 0 else 0
    minutes = int((time_to_sunset.seconds % 3600) / 60) if time_to_sunset.total_seconds() > 0 else 0
    
    return f"""
🌅 *Вечерний отчёт - {datetime.now(TIMEZONE).strftime('%H:%M')}*

🌊 *Условия сейчас:*
🌡 Вода: 29.5°C
🌬 Ветер: 12 км/ч
🌊 Волны: 0.8 м
☁️ Погода: Ясно
🌡 Воздух: 30°C

🌅 *До заката: {hours}ч {minutes}мин*

🏖️ *Идеально для:*
• Вечернего купания
• Фотосессии
• SUP-бординга

🌴 *Вечерняя активность:*
🐢 Черепахи выходят на берег
🦜 Птицы-носороги возвращаются
    """

# Генерация прогноза на завтра
def get_tomorrow_forecast():
    tomorrow = (datetime.now(TIMEZONE) + timedelta(days=1)).strftime('%d.%m')
    
    return f"""
🌙 *Прогноз на завтра, {tomorrow}*

📊 *Ожидаемые условия:*
🌤 Погода: Переменная облачность
🌡 Воздух: 27-33°C
🌡 Вода: 29°C
🌬 Ветер: 10-15 км/ч
🌊 Волны: 0.7-1.0 м

🌊 *Приливы завтра:*
📈 Приливы: 05:54, 19:18
📉 Отливы: 11:45, 23:56

🎯 *Лучшее время для:*
🏊 Купания: 6:00-10:00, 17:00-19:00
🏄 Сёрфинга: 6:00-8:00
📸 Фото: 5:43-6:30, 18:00-18:46
🎣 Рыбалки: условия хорошие

Спокойной ночи! 🌴
    """

# Функции для автопостинга
def morning_report():
    send_to_all(get_morning_report())

def noon_update():
    send_to_all(get_noon_update())

def evening_update():
    send_to_all(get_evening_update())

def tomorrow_forecast():
    send_to_all(get_tomorrow_forecast())

# Обработчик команды start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn1 = types.KeyboardButton("🌊 Условия сейчас")
    btn2 = types.KeyboardButton("📅 Прогноз на завтра")
    btn3 = types.KeyboardButton("🏄 Активности")
    btn4 = types.KeyboardButton("🎣 Рыбалка")
    btn5 = types.KeyboardButton("📸 Фото-гид")
    btn6 = types.KeyboardButton("☀️ УФ-индекс")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    bot.send_message(
        message.chat.id,
        "🏖️ Салют, солнечный человек!\n\n"
        "Я твой пляжный помощник для Пхукета! 🏝️\n"
        "Выбери, что тебя интересует:",
        reply_markup=markup
    )

# Обработчик кнопки "Условия сейчас"
@bot.message_handler(func=lambda message: message.text == "🌊 Условия сейчас")
def send_current(message):
    bot.send_message(message.chat.id, get_morning_report(), parse_mode='Markdown')

# Обработчик кнопки "Прогноз на завтра"
@bot.message_handler(func=lambda message: message.text == "📅 Прогноз на завтра")
def send_tomorrow(message):
    bot.send_message(message.chat.id, get_tomorrow_forecast(), parse_mode='Markdown')

# Настройка расписания
def setup_schedule():
    schedule.every().day.at("07:00").do(morning_report)
    schedule.every().day.at("12:00").do(noon_update)
    schedule.every().day.at("17:00").do(evening_update)
    schedule.every().day.at("20:00").do(tomorrow_forecast)
    
    print("📅 Расписание настроено")

# Функция для работы планировщика
def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Функция для запуска бота
def run_bot():
    setup_schedule()
    
    # Запускаем планировщик в отдельном потоке
    schedule_thread = threading.Thread(target=schedule_checker)
    schedule_thread.daemon = True
    schedule_thread.start()
    
    print("🤖 Бот запущен!")
    
    # Запускаем бота
    bot.polling(none_stop=True)

# Запуск Flask и бота
if __name__ == '__main__':
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем Flask
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
