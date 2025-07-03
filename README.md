# 🤖 Telegram GPT-Бот

Умный Telegram-бот с голосовыми сообщениями и поддержкой OpenAI GPT.

---

## 🚀 Возможности

👤 Для пользователей:
- ✍️ Общение в текстовом формате
- 🎙 Поддержка голосовых сообщений (STT → GPT → TTS)
- 🧠 Поддержка контекста диалога (до 30 сообщений)
- 💳 Оплата через команду `/buy`

🛠 Для админов:
- 📥 Выгрузка списка пользователей
- 📢 Массовая рассылка сообщений

---

## 🧩 Используемые технологии

- Python + [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
- OpenAI Chat Completion API
- OpenAI Text-to-Speech API
- Telegram Payments

---

## 📁 Структура

```
.
├── bot.py             # Логика бота и обработка сообщений
├── admin.py           # Админ-панель (рассылка, выгрузка)
├── config.py          # Настройки (токены, модель, admin ID)
├── conversations.json # История сообщений и данные пользователей
└── requirements.txt   # Зависимости
```

---

## ⚙️ Установка

```bash
git clone <repo-url>
cd <project-folder>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Заполните `config.py` с токенами и ключами.

---

## ▶️ Запуск

```bash
python bot.py
```

---

## 👥 Использование

- `/start` — начать
- Отправьте текст или голос — бот ответит
- `/buy` — оплатить услугу

---

## 🔐 Контекст и данные

- Контекст диалога хранится в `conversations.json`
- До 30 последних сообщений на ветку (`private:{user_id}` и др.)

---

## 📬 Контрибьюция

PR и улучшения приветствуются!

---

