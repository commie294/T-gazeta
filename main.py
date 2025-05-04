import telebot
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env (если он есть)
load_dotenv()

# Получаем токен бота и ID канала из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

if not BOT_TOKEN:
    print("Ошибка: Не найдена переменная окружения BOT_TOKEN")
    exit()
if not CHANNEL_ID:
    print("Ошибка: Не найдена переменная окружения CHANNEL_ID")
    exit()

# Убедитесь, что CHANNEL_ID является целым числом (и, вероятно, отрицательным)
try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    print(f"Ошибка: Некорректное значение CHANNEL_ID: {CHANNEL_ID}. Должно быть целым числом.")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)
user_messages = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне стихотворение, и я анонимно перешлю его в канал.")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    user_id = message.from_user.id
    user_messages[user_id] = message.text
    bot.reply_to(message, "Ваше сообщение будет анонимно отправлено. Нажмите /send для отправки.")

@bot.message_handler(commands=['send'])
def send_anonymous_message(message):
    user_id = message.from_user.id
    if user_id in user_messages:
        anonymous_message = user_messages[user_id]
        try:
            bot.send_message(CHANNEL_ID, anonymous_message)
            bot.reply_to(message, "Сообщение успешно отправлено!")
            del user_messages[user_id] # Очищаем сообщение после отправки
        except telebot.apihelper.ApiTelegramException as e:
            bot.reply_to(message, f"Произошла ошибка при отправке сообщения: {e}")
    else:
        bot.reply_to(message, "Вы еще не отправили мне сообщение для пересылки.")

if __name__ == '__main__':
    print("Бот запущен с токеном:", BOT_TOKEN, "и ID канала:", CHANNEL_ID)
    bot.polling(none_stop=True)
