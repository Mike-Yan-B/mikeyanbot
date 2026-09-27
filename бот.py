# -*- coding: utf-8 -*-
"""
🤖 AmyStyle Pro Bot — заказ сайтов, Telegram-ботов и презентаций
Автор: Майк Ян
Версия: 2.0
"""

import telebot
from telebot import types
import json
import os
from datetime import datetime

# ============================================================
#  НАСТРОЙКИ
# ============================================================
BOT_TOKEN = "8867117495:AAF6khWZU6UVwQuxjPasqFRENErFPGiYiTg"

YOUR_USERNAME = "@mikkurdano_1"
YOUR_CHAT_ID = 6107364623

# 🖼️ Фото примеров (положи рядом с bot.py)
PHOTO_SIMPLE_SITE = "price_simple.jpg"
PHOTO_BOT = "price_bot.jpg"
PHOTO_PRESENTATION = "price_presentation.jpg"
PHOTO_WELCOME = "welcome.jpg"  # опционально — баннер приветствия

# 📁 Файл для сохранения заявок
ORDERS_FILE = "orders.json"

bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище состояний анкет пользователей
user_states = {}   # {chat_id: {"step": ..., "data": {...}}}


# ============================================================
#  УТИЛИТЫ
# ============================================================

def save_order(order: dict):
    """Сохраняет заявку в JSON-файл"""
    orders = []
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                orders = json.load(f)
        except Exception:
            orders = []
    orders.append(order)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


def notify_admin(text: str):
    """Отправляет уведомление владельцу"""
    try:
        bot.send_message(YOUR_CHAT_ID, text, parse_mode="HTML")
    except Exception as e:
        print(f"⚠️ Не удалось уведомить админа: {e}")


# ============================================================
#  КЛАВИАТУРЫ
# ============================================================

def main_menu():
    """Главное меню (Reply-кнопки)"""
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton("🛍 Услуги и цены"),
        types.KeyboardButton("📸 Портфолио"),
    )
    kb.add(
        types.KeyboardButton("📝 Оставить заявку"),
        types.KeyboardButton("⭐ Отзывы"),
    )
    kb.add(
        types.KeyboardButton("❓ FAQ"),
        types.KeyboardButton("🎁 Акции"),
    )
    kb.add(
        types.KeyboardButton("📞 Связаться"),
        types.KeyboardButton("ℹ️ О разработчике"),
    )
    return kb


def services_menu():
    """Инлайн-меню услуг"""
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🌐 Сайты — от 1500 ₽", callback_data="svc_site"),
        types.InlineKeyboardButton("🤖 Telegram-боты — от 1000 ₽", callback_data="svc_bot"),
        types.InlineKeyboardButton("🎞 Презентации — от 800 ₽", callback_data="svc_pres"),
        types.InlineKeyboardButton("◀️ В меню", callback_data="back_main"),
    )
    return kb


def back_menu():
    """Кнопка возврата в главное меню"""
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("◀️ В меню", callback_data="back_main"))
    return kb


def order_confirm_menu():
    """Меню подтверждения заявки"""
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Отправить", callback_data="order_send"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="order_cancel"),
    )
    return kb


# ============================================================
#  КОМАНДЫ
# ============================================================

@bot.message_handler(commands=["start"])
def cmd_start(message):
    user_states.pop(message.chat.id, None)
    name = message.from_user.first_name or "друг"

  text = (
    f"👋 <b>Привет, {name}!</b>\n\n"
    f"Добро пожаловать в <b>Mike Yan</b> 💼\n\n"
    f"Я — бот-помощник веб-разработчика <b>Майка Яна</b>.\n"
        f"Помогу тебе:\n\n"
        f"🌐 Заказать <b>сайт</b> — от 1500 ₽\n"
        f"🤖 Заказать <b>Telegram-бота</b> — от 1000 ₽\n"
        f"🎞 Заказать <b>презентацию</b> — от 800 ₽\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 <i>30+ успешных проектов</i>\n"
        f"⚡️ <i>Быстрые сроки — от 1 дня</i>\n"
        f"🛠 <i>Поддержка после запуска</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Выбери действие в меню ниже 👇"
    )

    try:
        with open(PHOTO_WELCOME, "rb") as photo:
            bot.send_photo(message.chat.id, photo,
                           caption=text, parse_mode="HTML",
                           reply_markup=main_menu())
    except FileNotFoundError:
        bot.send_message(message.chat.id, text, parse_mode="HTML",
                         reply_markup=main_menu())


@bot.message_handler(commands=["help"])
def cmd_help(message):
    cmd_start(message)


@bot.message_handler(commands=["menu"])
def cmd_menu(message):
    bot.send_message(message.chat.id, "🏠 Главное меню:",
                     reply_markup=main_menu())


@bot.message_handler(commands=["myid"])
def cmd_myid(message):
    bot.send_message(message.chat.id,
                     f"Ваш chat_id: <code>{message.chat.id}</code>",
                     parse_mode="HTML")


# ============================================================
#  КНОПКИ ГЛАВНОГО МЕНЮ
# ============================================================

@bot.message_handler(func=lambda m: m.text == "🛍 Услуги и цены")
def btn_services(message):
    text = (
        "🛍 <b>Услуги и цены</b>\n\n"
        "Выберите категорию — покажу цены и примеры 👇"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML",
                     reply_markup=services_menu())


@bot.message_handler(func=lambda m: m.text == "📸 Портфолио")
def btn_portfolio(message):
    text = (
        "📸 <b>Портфолио</b>\n\n"
        "Вот примеры моих работ 👇\n\n"
        "🌐 <b>Сайты</b> — лендинги, визитки, магазины\n"
        "🤖 <b>Боты</b> — магазины, заявки, автоответы\n"
        "🎞 <b>Презентации</b> — для бизнеса и учёбы\n\n"
        "Хочешь такой же? Жми <b>📝 Оставить заявку</b>!"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📝 Оставить заявку", callback_data="start_order"))

    # Пытаемся отправить фото, если есть
    sent = False
    for photo_file in [PHOTO_SIMPLE_SITE, PHOTO_BOT, PHOTO_PRESENTATION]:
        if os.path.exists(photo_file):
            try:
                with open(photo_file, "rb") as p:
                    bot.send_photo(message.chat.id, p)
                sent = True
            except Exception as e:
                print(f"Ошибка фото {photo_file}: {e}")

    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=kb)


@bot.message_handler(func=lambda m: m.text == "📝 Оставить заявку")
def btn_order(message):
    start_order_form(message)


@bot.message_handler(func=lambda m: m.text == "⭐ Отзывы")
def btn_reviews(message):
    text = (
        "⭐ <b>Отзывы клиентов</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "«Сделал сайт за 2 дня, всё чётко! Рекомендую 🔥»\n"
        "— <i>Анна, магазин цветов</i>\n\n"
        "«Бот работает как часы, заявки приходят сразу»\n"
        "— <i>Игорь, студия ремонта</i>\n\n"
        "«Презентация получилась стильная, защита прошла на ура»\n"
        "— <i>Мария, студентка</i>\n\n"
        "«Приятно работать, всё быстро и качественно»\n"
        "— <i>Дмитрий, ИП</i>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "💬 Хочешь оставить свой отзыв? Напиши мне!"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "✉️ Написать отзыв",
        url=f"https://t.me/{YOUR_USERNAME.lstrip('@')}"
    ))
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=kb)


@bot.message_handler(func=lambda m: m.text == "❓ FAQ")
def btn_faq(message):
    text = (
        "❓ <b>Частые вопросы</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⏱ <b>Сколько ждать заказ?</b>\n"
        "Сайт — 1–3 дня, бот — 1–2 дня, презентация — 1 день.\n\n"
        "💳 <b>Как оплатить?</b>\n"
        "50% предоплата, остальное — после сдачи. Перевод на карту / СБП.\n\n"
        "🔧 <b>Делаешь ли правки?</b>\n"
        "Да, бесплатные правки до результата.\n\n"
        "🌍 <b>Работаешь по всей России?</b>\n"
        "Да, работаю удалённо со всем миром 🌍\n\n"
        "📦 <b>Что входит в стоимость?</b>\n"
        "Разработка, запуск, хостинг (для бота), поддержка.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "Не нашёл ответ? Жми <b>📞 Связаться</b>!"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML",
                     reply_markup=back_menu())


@bot.message_handler(func=lambda m: m.text == "🎁 Акции")
def btn_promo(message):
    text = (
        "🎁 <b>Акции и бонусы</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔥 <b>1. Скидка 15% на второй заказ</b>\n"
        "Закажи что-то повторно — получи скидку 15%!\n\n"
        "👥 <b>2. Приведи друга — 500 ₽</b>\n"
        "Приведи друга — он получит скидку 500 ₽,\n"
        "а ты — бонус на следующий заказ.\n\n"
        "⚡️ <b>3. Срочный заказ за 24 часа</b>\n"
        "Нужно срочно? Сделаю за сутки (+30% к цене).\n\n"
        "📦 <b>4. Пакет «Всё под ключ»</b>\n"
        "Сайт + бот + презентация = <b>скидка 20%</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "💬 Хочешь воспользоваться? Пиши мне!"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "✉️ Воспользоваться акцией",
        url=f"https://t.me/{YOUR_USERNAME.lstrip('@')}"
    ))
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=kb)


@bot.message_handler(func=lambda m: m.text == "📞 Связаться")
def btn_contact(message):
    text = (
        "📞 <b>Связаться со мной</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 Telegram: <b>{YOUR_USERNAME}</b>\n"
        f"💬 Отвечаю в течение 15–30 минут\n\n"
        f"Напишите, что нужно — обсудим детали и сроки! 🚀"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "✉️ Написать в Telegram",
        url=f"https://t.me/{YOUR_USERNAME.lstrip('@')}"
    ))
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=kb)


@bot.message_handler(func=lambda m: m.text == "ℹ️ О разработчике")
def btn_about(message):
    text = (
        "👨‍💻 <b>О разработчике</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👋 Привет! Я — <b>Майк Ян</b>\n"
        "<i>Full-Stack Web Developer</i>\n\n"
        "📊 <b>Опыт:</b> 4+ года в веб-разработке\n"
        "🚀 <b>Сделано:</b> 30+ успешных проектов\n"
        "⭐️ <b>Рейтинг:</b> 5.0 из 5\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "💼 <b>Специализация:</b>\n"
        "• Сайты-визитки и лендинги\n"
        "• Интернет-магазины\n"
        "• CRM и веб-приложения\n"
        "• Telegram-боты любой сложности\n"
        "• Презентации для бизнеса и учёбы\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 <b>Связь:</b> {YOUR_USERNAME}\n"
        f"⏱ <b>Ответ:</b> 15–30 минут"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")


# ============================================================
#  INLINE CALLBACK
# ============================================================

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = call.data

    if data == "back_main":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🏠 Главное меню:",
                         reply_markup=main_menu())

    elif data == "svc_site":
        send_prices_sites(call.message)
        bot.answer_callback_query(call.id, "🌐 Цены на сайты")

    elif data == "svc_bot":
        send_prices_bots(call.message)
        bot.answer_callback_query(call.id, "🤖 Цены на ботов")

    elif data == "svc_pres":
        send_prices_presentations(call.message)
        bot.answer_callback_query(call.id, "🎞 Цены на презентации")

    elif data == "order_site":
        start_order_form(call.message, kind="site")
        bot.answer_callback_query(call.id, "🌐 Оформляем заказ сайта")

    elif data == "order_bot":
        start_order_form(call.message, kind="bot")
        bot.answer_callback_query(call.id, "🤖 Оформляем заказ бота")

    elif data == "order_pres":
        start_order_form(call.message, kind="presentation")
        bot.answer_callback_query(call.id, "🎞 Оформляем заказ презентации")

    elif data == "start_order":
        start_order_form(call.message)
        bot.answer_callback_query(call.id)

    elif data == "order_send":
        finish_order(call.message)
        bot.answer_callback_query(call.id, "✅ Заявка отправлена!")

    elif data == "order_cancel":
        user_states.pop(call.message.chat.id, None)
        bot.send_message(call.message.chat.id,
                         "❌ Заявка отменена.",
                         reply_markup=main_menu())
        bot.answer_callback_query(call.id, "Отменено")


# ============================================================
#  ЦЕНЫ
# ============================================================

def send_prices_sites(message):
    text = (
        "💰 <b>Цены на создание сайтов</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌐 <b>Обычный сайт (1 слайд)</b>\n"
        "   Одностраничник, аккуратный дизайн\n"
        "   💵 <b>1500 ₽</b>\n\n"
        "🌐 <b>Сайт на 2 слайда</b>\n"
        "   Больше секций и фотографий\n"
        "   💵 <b>2500 ₽</b>\n\n"
        "🌐 <b>Сайт на 3 слайда</b>\n"
        "   Расширенная версия с анимациями\n"
        "   💵 <b>3500 ₽</b>\n\n"
        "🌐 <b>Сайт на 4 слайда</b>\n"
        "   Многофункциональный сайт\n"
        "   💵 <b>4500 ₽</b>\n\n"
        "🌐 <b>Сайт на 5 слайдов</b>\n"
        "   Полноценный сайт с админкой\n"
        "   💵 <b>5500 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡️ <b>Входит в стоимость:</b>\n"
        "• Современный дизайн\n"
        "• Адаптив под телефон\n"
        "• Бесплатные правки\n"
        "• Помощь с хостингом\n\n"
        "Хочешь заказать? 👇"
    )

    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🌐 Заказать сайт", callback_data="order_site"),
        types.InlineKeyboardButton("◀️ К услугам", callback_data="back_services"),
    )

    try:
        with open(PHOTO_SIMPLE_SITE, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=text,
                           parse_mode="HTML", reply_markup=kb)
    except FileNotFoundError:
        bot.send_message(message.chat.id, text, parse_mode="HTML",
                         reply_markup=kb)


def send_prices_bots(message):
    text = (
        "🤖 <b>Цены на Telegram-ботов</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🤖 <b>Бот с любым функционалом</b>\n"
        "   💵 <b>1000 ₽</b>\n\n"
        "⚡️ <b>Что может бот:</b>\n"
        "• Автоответы и меню\n"
        "• Приём заявок и заказов\n"
        "• Уведомления вам в личку\n"
        "• Кнопки, команды, рассылки\n"
        "• Оплата внутри бота\n"
        "• Любой функционал под задачу\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡️ <b>Входит в стоимость:</b>\n"
        "• Разработка под ваши задачи\n"
        "• Настройка и запуск\n"
        "• Хостинг 24/7 (бот работает всегда)\n"
        "• Поддержка после запуска\n\n"
        "Хочешь заказать? 👇"
    )

    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🤖 Заказать бота", callback_data="order_bot"),
        types.InlineKeyboardButton("◀️ К услугам", callback_data="back_services"),
    )

    try:
        with open(PHOTO_BOT, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=text,
                           parse_mode="HTML", reply_markup=kb)
    except FileNotFoundError:
        bot.send_message(message.chat.id, text, parse_mode="HTML",
                         reply_markup=kb)


def send_prices_presentations(message):
    text = (
        "🎞 <b>Цены на презентации</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎞 <b>5–7 слайдов</b>\n"
        "   Для короткого выступления или питча\n"
        "   💵 <b>800 ₽</b>\n\n"
        "🎞 <b>8–10 слайдов</b>\n"
        "   Для бизнеса, услуг или учёбы\n"
        "   💵 <b>1000 ₽</b>\n\n"
        "🎞 <b>11–15 слайдов</b>\n"
        "   Расширенная с подробным дизайном\n"
        "   💵 <b>1500 ₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡️ <b>Входит в стоимость:</b>\n"
        "• Современный дизайн\n"
        "• Подбор шрифтов и цветов\n"
        "• Структура и логика слайдов\n"
        "• Анимации и переходы\n"
        "• Правки до результата\n\n"
        "Хочешь заказать? 👇"
    )

    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🎞 Заказать презентацию", callback_data="order_pres"),
        types.InlineKeyboardButton("◀️ К услугам", callback_data="back_services"),
    )

    try:
        with open(PHOTO_PRESENTATION, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=text,
                           parse_mode="HTML", reply_markup=kb)
    except FileNotFoundError:
        bot.send_message(message.chat.id, text, parse_mode="HTML",
                         reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data == "back_services")
def back_to_services(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,
                     "🛍 <b>Услуги и цены</b>\n\nВыберите категорию:",
                     parse_mode="HTML",
                     reply_markup=services_menu())


# ============================================================
#  АНКЕТА ЗАКАЗА (FSM)
# ============================================================

STEPS = {
    "kind": "🎯 Что вы хотите заказать?",
    "name": "👤 Как вас зовут?",
    "contact": "📞 Ваш телефон или @username для связи:",
    "desc": "📝 Опишите задачу — что нужно сделать?",
    "budget": "💰 Ваш бюджет (или напишите «не знаю»):",
    "deadline": "⏱ Когда нужно? (сроки)",
}


def start_order_form(message, kind=None):
    """Начинает анкету заказа"""
    chat_id = message.chat.id
    user_states[chat_id] = {
        "step": "kind" if not kind else "name",
        "data": {"kind": kind} if kind else {}
    }

    if kind:
        kind_ru = {"site": "Сайт", "bot": "Telegram-бот",
                   "presentation": "Презентация"}.get(kind, "Услуга")
        bot.send_message(chat_id,
                         f"📝 <b>Оформление заявки</b>\n\n"
                         f"Услуга: <b>{kind_ru}</b>\n\n"
                         f"{STEPS['name']}",
                         parse_mode="HTML",
                         reply_markup=types.ReplyKeyboardRemove())
    else:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kb.add(types.KeyboardButton("🌐 Сайт"))
        kb.add(types.KeyboardButton("🤖 Telegram-бот"))
        kb.add(types.KeyboardButton("🎞 Презентация"))
        bot.send_message(chat_id,
                         f"📝 <b>Оформление заявки</b>\n\n{STEPS['kind']}",
                         parse_mode="HTML", reply_markup=kb)


@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "kind")
def step_kind(message):
    chat_id = message.chat.id
    text = message.text.lower()

    if "сайт" in text:
        kind = "site"
    elif "бот" in text:
        kind = "bot"
    elif "презентац" in text:
        kind = "presentation"
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите из кнопок 👇")
        return

    user_states[chat_id]["data"]["kind"] = kind
    user_states[chat_id]["step"] = "name"
    bot.send_message(chat_id, STEPS["name"],
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "name")
def step_name(message):
    chat_id = message.chat.id
    user_states[chat_id]["data"]["name"] = message.text
    user_states[chat_id]["step"] = "contact"
    bot.send_message(chat_id, STEPS["contact"])


@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "contact")
def step_contact(message):
    chat_id = message.chat.id
    user_states[chat_id]["data"]["contact"] = message.text
    user_states[chat_id]["step"] = "desc"
    bot.send_message(chat_id, STEPS["desc"])


@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "desc")
def step_desc(message):
    chat_id = message.chat.id
    user_states[chat_id]["data"]["desc"] = message.text
    user_states[chat_id]["step"] = "budget"
    bot.send_message(chat_id, STEPS["budget"])


@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "budget")
def step_budget(message):
    chat_id = message.chat.id
    user_states[chat_id]["data"]["budget"] = message.text
    user_states[chat_id]["step"] = "deadline"
    bot.send_message(chat_id, STEPS["deadline"])


@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "deadline")
def step_deadline(message):
    chat_id = message.chat.id
    user_states[chat_id]["data"]["deadline"] = message.text
    user_states[chat_id]["step"] = "confirm"

    data = user_states[chat_id]["data"]
    kind_ru = {"site": "🌐 Сайт", "bot": "🤖 Telegram-бот",
               "presentation": "🎞 Презентация"}.get(data.get("kind"), "—")

    preview = (
        f"📋 <b>Проверьте заявку</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🎯 Услуга: <b>{kind_ru}</b>\n"
        f"👤 Имя: <b>{data.get('name', '—')}</b>\n"
        f"📞 Контакт: <b>{data.get('contact', '—')}</b>\n"
        f"📝 Задача: {data.get('desc', '—')}\n"
        f"💰 Бюджет: <b>{data.get('budget', '—')}</b>\n"
        f"⏱ Сроки: <b>{data.get('deadline', '—')}</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"Всё верно? Нажмите <b>✅ Отправить</b>"
    )
    bot.send_message(chat_id, preview, parse_mode="HTML",
                     reply_markup=order_confirm_menu())


def finish_order(message):
    """Отправляет заявку админу"""
    chat_id = message.chat.id
    if chat_id not in user_states:
        return

    data = user_states[chat_id]["data"]
    user = message.from_user
    username = f"@{user.username}" if user.username else "без username"

    kind_ru = {"site": "🌐 Сайт", "bot": "🤖 Telegram-бот",
               "presentation": "🎞 Презентация"}.get(data.get("kind"), "—")

    # Уведомление админу
    order_text = (
        f"🔔 <b>НОВАЯ ЗАЯВКА!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🎯 Услуга: <b>{kind_ru}</b>\n"
        f"👤 Имя: <b>{data.get('name', '—')}</b>\n"
        f"📞 Контакт: <b>{data.get('contact', '—')}</b>\n"
        f"📝 Задача: {data.get('desc', '—')}\n"
        f"💰 Бюджет: <b>{data.get('budget', '—')}</b>\n"
        f"⏱ Сроки: <b>{data.get('deadline', '—')}</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 Username: {username}\n"
        f"🆔 chat_id: <code>{user.id}</code>\n"
        f"🔗 <a href='tg://user?id={user.id}'>Написать клиенту</a>\n"
        f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )
    notify_admin(order_text)

    # Сохраняем в файл
    save_order({
        "time": datetime.now().isoformat(),
        "user_id": user.id,
        "username": username,
        "kind": data.get("kind"),
        "name": data.get("name"),
        "contact": data.get("contact"),
        "desc": data.get("desc"),
        "budget": data.get("budget"),
        "deadline": data.get("deadline"),
    })

    # Подтверждение клиенту
    bot.send_message(
        chat_id,
        f"✅ <b>Заявка отправлена!</b>\n\n"
        f"Спасибо, {data.get('name', '')}! 🎉\n\n"
        f"Я получил вашу заявку и свяжусь с вами "
        f"в течение 15–30 минут.\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💬 Хотите ускорить? Напишите мне:\n"
        f"👉 <b>{YOUR_USERNAME}</b>",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

    user_states.pop(chat_id, None)


# ============================================================
#  ЛЮБОЙ ДРУГОЙ ТЕКСТ (вне анкеты)
# ============================================================

@bot.message_handler(content_types=["text"])
def fallback_text(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "без username"

    bot.send_message(
        message.chat.id,
        "✅ <b>Сообщение получено!</b>\n\n"
        "Передал его разработчику — скоро ответит.\n"
        f"Хотите быстрее? Напишите напрямую: <b>{YOUR_USERNAME}</b>\n\n"
        "Или выберите действие в меню 👇",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

    notify_admin(
        f"💬 <b>Сообщение от клиента</b>\n\n"
        f"👤 {user.first_name or ''} {user.last_name or ''}\n"
        f"🔗 {username}\n"
        f"🆔 <code>{user.id}</code>\n\n"
        f"💬 {message.text}"
    )


# ============================================================
#  ЗАПУСК
# ============================================================

if __name__ == "__main__":
    print("=" * 55)
    print("  🤖  AmyStyle Pro Bot v2.0 запущен!")
    print("  📱  Открой бота в Telegram и напиши /start")
    print("=" * 55)
    bot.infinity_polling()
