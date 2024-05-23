import logging
import sqlite3
import openai
from telebot import TeleBot

# Настройка детального логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Токены API
TELEGRAM_TOKEN = '_______________'
OPENAI_API_KEY = '_______________'

# Инициализация OpenAI API
openai.api_key = OPENAI_API_KEY

# Инициализация бота Telegram
bot = TeleBot(TELEGRAM_TOKEN)


# Создание таблицы для хранения истории сообщений
def create_table():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (user_id INTEGER, business_connection_id TEXT, message_role TEXT, message_content TEXT)''')
    conn.commit()
    conn.close()


# Сохранение сообщения в базу данных
def save_message(user_id, business_connection_id, message_role, message_content):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_history (user_id, business_connection_id, message_role, message_content) VALUES (?, ?, ?, ?)",
        (user_id, business_connection_id, message_role, message_content))
    conn.commit()
    conn.close()


# Получение истории сообщений для определенного пользователя и бизнес-соединения
def get_chat_history(user_id, business_connection_id):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute(
        "SELECT message_role, message_content FROM chat_history WHERE user_id=? AND business_connection_id=? ORDER BY rowid",
        (user_id, business_connection_id))
    chat_history = c.fetchall()
    conn.close()
    return chat_history


# Обработчик бизнес-соединений
@bot.business_message_handler(func=lambda message: True, content_types=['text', 'photo', 'video'])
def handle_business_message(message):
    user_id = message.chat.id
    business_connection_id = message.business_connection_id
    logging.info(f"Received business message from {user_id}: {message.text}")

    try:
        # Сохранение входящего сообщения в базу данных
        save_message(user_id, business_connection_id, 'user', message.text)

        # Получение истории сообщений из базы данных
        chat_history = get_chat_history(user_id, business_connection_id)
        messages = [
            {"role": "system",
             "content": "Привет! Ты - ИИ-помощник для бизнеса в Telegram. Отвечай на вопросы пользователей по этому сценарию: Привет! Я ваш помощник, созданный для помощи вашему бизнесу. "
                        "Меня зовут Yakov's Assistant. Если у вас есть вопросы или вам нужна помощь, не стесняйтесь обращаться ко мне. Я чат-бот, который использует весь потенциал OpenAI для обеспечения наилучшего опыта общения с вами. "
                        "Я могу помочь вам создать бота для вашего бизнеса с использованием всех возможностей OpenAI. Мой создатель, Yakov Maurer, опытный программист и разработчик чат-ботов, стоит за моей разработкой. "
                        "Не забывайте, что помимо моих возможностей, мой создатель, Yakov Maurer, также является опытным программистом. Его навыки включают работу с Python, базами данных и разработку чат-ботов для различных направлений бизнеса. "
                        "Мой создатель, Yakov Maurer, имеет опыт в программно-административной работе и обеспечении корректной работы сервиса. Он владеет Python на уровне Junior, работал с базами данных и разрабатывал Telegram ботов и скрипты для разных направлений бизнеса. "
                        "Если у вас возникли вопросы или вам нужна дополнительная информация, вы можете связаться с Yakov Maurer через [Telegram](https://t.me/maureryakov) или [Facebook](https://www.facebook.com/maureryakov)"},
            *[{"role": role, "content": content} for role, content in chat_history]
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            temperature=0.8,
        )
        message_text = response.choices[0].message.content

        # Сохранение ответа бота в базу данных
        save_message(user_id, business_connection_id, 'assistant', message_text)

        bot.send_message(message.chat.id, message_text, reply_to_message_id=message.id,
                         business_connection_id=business_connection_id)
        logging.info("Response sent to business chat")
    except Exception as e:
        logging.error(f"Error generating or sending response to business chat: {e}")


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    logging.debug("Handling /start command")
    bot.reply_to(message, "Привет! Я ваш бот.")


if __name__ == "__main__":
    create_table()  # Создание таблицы для хранения истории сообщений
    logging.info("Starting the bot")
    bot.infinity_polling()
