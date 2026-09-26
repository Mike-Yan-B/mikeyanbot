# -*- coding: utf-8 -*-
"""
Telegram-бот для заказов сайтов, Telegram-ботов и презентаций.
Автор: Майк Ян
"""

import telebot
from telebot import types

# ============================================================
#  НАСТРОЙКИ
# ============================================================

# ⚠️ ЗАМЕНИТЕ на новый токен после /revoke у @BotFather
BOT_TOKEN = "8867117495:AAF6khWZU6UVwQuxjPasqFRENErFPGiYiTg"

# 👤 Ваш Telegram-юзернейм
YOUR_USERNAME = "@mikkurdano_1"

# 📩 Ваш chat_id — сюда будут приходить заявки
YOUR_CHAT_ID = 6107364623

# 🖼️ Фото примеров
PHOTO_SIMPLE_SITE = "price_simple.jpg"        # Пример обычного сайта (1 слайд)
PHOTO_BOT = "price_bot.jpg"                   # Пример Telegram-бота
PHOTO_PRESENTATION = "price_presentation.jpg" # Пример презентации

bot = telebot.TeleBot(BOT_TOKEN)


# ============================================================
#  КЛАВИАТУРЫ
# ============================================================

def main_menu():
    """Главное меню бота"""
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton("💰 Цены"),
        types.KeyboardButton("🎞 Презентации"),
    )
    kb.add(
        types.KeyboardButton("🌐 Заказать сайт"),
        types.KeyboardButton("🤖 Заказать бота"),
    )
    kb.add(
        types.KeyboardButton("🎞 Заказать презентацию"),
        types.KeyboardButton("📞 Связаться со мной"),
    )
    kb.add(
        types.KeyboardButton("ℹ️ О разработчике"),
    )
    return kb


def prices_menu():
    """Меню выбора категории цен"""
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🌐 Цены на сайты", callback_data="prices_sites"),
        types.InlineKeyboardButton("🤖 Цены на Telegram-ботов", callback_data="prices_bots"),
        types.InlineKeyboardButton("🎞 Цены на презентации", callback_data="prices_presentations"),
    )
    return kb


# ============================================================
#  КОМАНДЫ
# ============================================================

@bot.message_handler(commands=["start"])
def cmd_start(message):
    name = message.from_user.first_name or "друг"
    text = (
        f"👋 Привет, <b>{name}</b>!\n\n"
        f"Я — бот-помощник веб-разработчика <b>Майка Яна</b>.\n"
        f"Здесь ты можешь:\n\n"
        f"💰 <b>Посмотреть цены</b> на сайты, ботов и презентации\n"
        f"🌐 <b>Заказать сайт</b> — расскажи, что нужно\n"
        f"🤖 <b>Заказать Telegram-бота</b> — любой функционал\n"
        f"🎞 <b>Заказать презентацию</b> — 5–15 слайдов\n"
        f"📞 <b>Связаться</b> со мной напрямую\n\n"
        f"Выбери действие в меню ниже 👇"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML",
                     reply_markup=main_menu())


@bot.message_handler(commands=["help"])
def cmd_help(message):
    cmd_start(message)


@bot.message_handler(commands=["prices", "price"])
def cmd_prices(message):
    """Команда /prices — меню категорий цен"""
    bot.send_message(
        message.chat.id,
        "💰 <b>Что вас интересует?</b>\n\nВыберите категорию:",
        parse_mode="HTML",
        reply_markup=prices_menu()
    )


@bot.message_handler(commands=["myid"])
def cmd_myid(message):
    """Показывает chat_id пользователя (для отладки)"""
    bot.send_message(
        message.chat.id,
        f"Ваш chat_id: <code>{message.chat.id}</code>",
        parse_mode="HTML"
    )


# ============================================================
#  КНОПКИ
# ============================================================

@bot.message_handler(func=lambda m: m.text == "💰 Цены")
def btn_prices(message):
    cmd_prices(message)


@bot.message_handler(func=lambda m: m.text == "🎞 Презентации")
def btn_presentations(message):
    """Кнопка '🎞 Презентации' — сразу показывает цены на презентации"""
    send_prices_presentations(message)


@bot.message_handler(func=lambda m: m.text == "🌐 Заказать сайт")
def btn_order_site(message):
    send_order_info(message, kind="site")


@bot.message_handler(func=lambda m: m.text == "🤖 Заказать бота")
def btn_order_bot(message):
    send_order_info(message, kind="bot")


@bot.message_handler(func=lambda m: m.text == "🎞 Заказать презентацию")
def btn_order_presentation(message):
    send_order_info(message, kind="presentation")


@bot.message_handler(func=lambda m: m.text == "📞 Связаться со мной")
def btn_contact(message):
    text = (
        f"📞 <b>Связаться со мной</b>\n\n"
        f"Telegram: {YOUR_USERNAME}\n"
        f"Пишите — отвечу в ближайшее время!"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")


@bot.message_handler(func=lambda m: m.text == "ℹ️ О разработчике")
def btn_about(message):
    text = (
        f"👨‍💻 <b>О разработчике</b>\n\n"
        f"<b>Майк Ян</b> — Full-Stack Web Developer\n"
        f"Опыт: 4+ года в веб-разработке\n"
        f"Сделано: 30+ успешных проектов\n\n"
        f"<b>Специализация:</b>\n"
        f"• Сайты-визитки и лендинги\n"
        f"• Интернет-магазины\n"
        f"• CRM и веб-приложения\n"
        f"• Telegram-боты любой сложности\n"
        f"• Презентации для бизнеса и учёбы\n\n"
        f"🔗 Связь: {YOUR_USERNAME}"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")


# ============================================================
#  INLINE КНОПКИ (callback)
# ============================================================

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "prices_sites":
        send_prices_sites(call.message)
        bot.answer_callback_query(call.id, "Показываю цены на сайты 🌐")
    elif call.data == "prices_bots":
        send_prices_bots(call.message)
        bot.answer_callback_query(call.id, "Показываю цены на ботов 🤖")
    elif call.data == "prices_presentations":
        send_prices_presentations(call.message)
        bot.answer_callback_query(call.id, "Показываю цены на презентации 🎞")
    elif call.data == "order_site":
        send_order_info(call.message, kind="site")
        bot.answer_callback_query(call.id, "Заказ сайта 🌐")
    elif call.data == "order_bot":
        send_order_info(call.message, kind="bot")
        bot.answer_callback_query(call.id, "Заказ бота 🤖")
    elif call.data == "order_presentation":
        send_order_info(call.message, kind="presentation")
        bot.answer_callback_query(call.id, "Заказ презентации 🎞")


# ============================================================
#  ФУНКЦИИ ОТПРАВКИ — ЦЕНЫ
# ============================================================

def send_prices_sites(message):
    """Цены на сайты + фото примера"""
    text = (
        "💰 <b>Цены на создание сайтов</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌐 <b>Обычный сайт (1 слайд)</b>\n"
        "   Простой, аккуратный одностраничник\n"
        "   💵 <b>1500 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌐 <b>Сайт на 2 слайда</b>\n"
        "   Улучшенное меню, другой шрифт,\n"
        "   больше секций и фотографий\n"
        "   💵 <b>2500 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌐 <b>Сайт на 3 слайда</b>\n"
        "   Расширенная версия с анимациями\n"
        "   💵 <b>3500 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌐 <b>Сайт на 4 слайда</b>\n"
        "   Многофункциональный сайт\n"
        "   💵 <b>4500 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌐 <b>Сайт на 5 слайдов</b>\n"
        "   Полноценный сайт с админкой\n"
        "   💵 <b>5500 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📸 <i>Ниже — пример обычного сайта (1 слайд)</i>\n\n"
        "Чтобы заказать — нажми <b>🌐 Заказать сайт</b>"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🌐 Заказать сайт", callback_data="order_site"))

    try:
        with open(PHOTO_SIMPLE_SITE, "rb") as photo:
            bot.send_photo(message.chat.id, photo,
                           caption=text, parse_mode="HTML",
                           reply_markup=kb)
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            text + "\n\n⚠️ <i>(Фото-пример не найдено: положите "
                   "price_simple.jpg рядом с bot.py)</i>",
            parse_mode="HTML",
            reply_markup=kb,
        )


def send_prices_bots(message):
    """Цены на Telegram-ботов + фото примера"""
    text = (
        "🤖 <b>Цены на Telegram-ботов</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🤖 <b>Обычный бот с любыми функциями</b>\n"
        "   • Автоответы и меню\n"
        "   • Приём заявок и заказов\n"
        "   • Уведомления вам в личку\n"
        "   • Кнопки, команды, рассылки\n"
        "   • Любой функционал под вашу задачу\n\n"
        "   💵 <b>1000 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚡️ <b>Что входит в стоимость:</b>\n"
        "• Разработка под ваши задачи\n"
        "• Настройка и запуск\n"
        "• Хостинг 24/7 (бот работает всегда)\n"
        "• Поддержка после запуска\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📸 <i>Ниже — пример Telegram-бота</i>\n\n"
        "Чтобы заказать — нажми <b>🤖 Заказать бота</b>"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🤖 Заказать бота", callback_data="order_bot"))

    try:
        with open(PHOTO_BOT, "rb") as photo:
            bot.send_photo(message.chat.id, photo,
                           caption=text, parse_mode="HTML",
                           reply_markup=kb)
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            text + "\n\n⚠️ <i>(Фото-пример не найдено: положите "
                   "price_bot.jpg рядом с bot.py)</i>",
            parse_mode="HTML",
            reply_markup=kb,
        )


def send_prices_presentations(message):
    """Цены на презентации + фото примера"""
    text = (
        "🎞 <b>Цены на презентации</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎞 <b>Презентация на 5–7 слайдов</b>\n"
        "   Небольшая презентация для выступления,\n"
        "   защиты проекта или короткого питча\n"
        "   💵 <b>800 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎞 <b>Презентация на 8–10 слайдов</b>\n"
        "   Презентация для бизнеса, услуг\n"
        "   или учебного проекта\n"
        "   💵 <b>1000 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎞 <b>Презентация на 11–15 слайдов</b>\n"
        "   Расширенная презентация с подробным\n"
        "   раскрытием темы и дизайном\n"
        "   💵 <b>1500 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚡️ <b>Что входит в стоимость:</b>\n"
        "• Красивый современный дизайн\n"
        "• Подбор шрифтов и цветовой схемы\n"
        "• Структура и логика слайдов\n"
        "• Анимации и переходы\n"
        "• Правки до результата\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📸 <i>Ниже — пример презентации</i>\n\n"
        "Чтобы заказать — нажми <b>🎞 Заказать презентацию</b>"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🎞 Заказать презентацию",
                                      callback_data="order_presentation"))

    try:
        with open(PHOTO_PRESENTATION, "rb") as photo:
            bot.send_photo(message.chat.id, photo,
                           caption=text, parse_mode="HTML",
                           reply_markup=kb)
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            text + "\n\n⚠️ <i>(Фото-пример не найдено: положите "
                   "price_presentation.jpg рядом с bot.py)</i>",
            parse_mode="HTML",
            reply_markup=kb,
        )


# ============================================================
#  ФУНКЦИИ ОТПРАВКИ — ЗАКАЗЫ
# ============================================================

def send_order_info(message, kind="site"):
    """
    Отправляет информацию о заказе.
    kind = "site"          — заказ сайта
    kind = "bot"           — заказ Telegram-бота
    kind = "presentation"  — заказ презентации
    """
    if kind == "site":
        header = "🌐 <b>Заказ сайта</b>"
        what = "сайт"
        hints = (
            "📝 <b>Что мне полезно знать:</b>\n"
            "• Тематика сайта (магазин / визитка / блог)\n"
            "• Сколько примерно страниц (слайдов)\n"
            "• Есть ли примеры сайтов, которые нравятся\n"
            "• Ваши контакты для связи"
        )
    elif kind == "bot":
        header = "🤖 <b>Заказ Telegram-бота</b>"
        what = "бота"
        hints = (
            "📝 <b>Что мне полезно знать:</b>\n"
            "• Для чего нужен бот (магазин / заявки / рассылка)\n"
            "• Какие функции должны быть\n"
            "• Нужна ли оплата внутри бота\n"
            "• Есть ли примеры ботов, которые нравятся"
        )
    else:  # presentation
        header = "🎞 <b>Заказ презентации</b>"
        what = "презентацию"
        hints = (
            "📝 <b>Что мне полезно знать:</b>\n"
            "• Тема презентации\n"
            "• Сколько нужно слайдов (5–7 / 8–10 / 11–15)\n"
            "• Для чего (бизнес / учёба / питч)\n"
            "• Есть ли примеры стиля, который нравится"
        )

    text = (
        f"{header}\n\n"
        f"Здравствуйте! 👋\n\n"
        f"Если вы хотите заказать {what} — напишите мне лично:\n"
        f"👉 <b>{YOUR_USERNAME}</b>\n\n"
        f"Либо <b>напишите текстом прямо сюда</b>, что за {what} вы хотите "
        f"(задачи, стиль, функционал, примеры) — "
        f"я его в ближайшее время сделаю! 🚀\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"{hints}\n\n"
        f"Жду ваше сообщение! ✨"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        text="✉️ Написать мне в Telegram",
        url=f"https://t.me/{YOUR_USERNAME.lstrip('@')}"
    ))

    bot.send_message(message.chat.id, text,
                     parse_mode="HTML", reply_markup=kb)


# ============================================================
#  ЛЮБОЙ ТЕКСТ = ЗАЯВКА
# ============================================================

@bot.message_handler(content_types=["text"])
def any_text(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "без username"

    # Подтверждение пользователю
    bot.send_message(
        message.chat.id,
        "✅ <b>Спасибо! Ваша заявка получена.</b>\n\n"
        "Я передал её разработчику — он свяжется с вами в ближайшее время.\n"
        f"Если хотите ускорить — напишите напрямую: <b>{YOUR_USERNAME}</b>",
        parse_mode="HTML",
    )

    # Уведомление вам
    try:
        bot.send_message(
            YOUR_CHAT_ID,
            f"🔔 <b>Новая заявка!</b>\n\n"
            f"👤 Имя: <b>{user.first_name or ''} {user.last_name or ''}</b>\n"
            f"🔗 Username: {username}\n"
            f"🆔 chat_id: <code>{user.id}</code>\n"
            f"💬 Сообщение:\n\n{message.text}",
            parse_mode="HTML",
        )
    except Exception as e:
        print(f"Не удалось переслать заявку: {e}")


# ============================================================
#  ЗАПУСК
# ============================================================

if __name__ == "__main__":
    print("=" * 55)
    print("  🤖  Telegram-бот 'Заказ сайтов, ботов и презентаций' запущен!")
    print("  📱  Открой бота в Telegram и напиши /start")
    print("=" * 55)
    bot.infinity_polling()