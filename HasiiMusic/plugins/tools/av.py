# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# All rights reserved.
#
# Bu kod, Nand Yaduwanshi'nin fikrî mülkiyetidir.
# Açık izin olmadan bu kodu kopyalamak, değiştirmek, yeniden dağıtmak
# veya ticari/kişisel projelerde kullanmak yasaktır.
#
# İzin Verilenler:
# - Kişisel öğrenme amacıyla fork etmek
# - Pull request ile iyileştirme göndermek
#
# İzin Verilmeyenler:
# - Kodu kendinize aitmiş gibi göstermek
# - İzin ve/veya kredi vermeden yeniden yüklemek
# - Satmak veya ticari olarak kullanmak
#
# İzinler için iletişim:
# E-posta: badboy809075@gmail.com
#
# Not: Bu dosyada yalnızca kullanıcıya görünen metinler Türkçeleştirilmiştir.

import random
import requests
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from HasiiMusic import app


# ────────────────────────────────────────────────
# 🎲 DİCE / OYUN EMOJİLERİ
# ────────────────────────────────────────────────

@app.on_message(
    filters.command(
        [
            "dice",
            "ludo",
            "dart",
            "basket",
            "basketball",
            "futbol",
            "football",
            "slot",
            "bowling",
            "jackpot",
        ],
        prefixes=["/"],
    )
)
async def dice(c, m: Message):
    command = m.text.split()[0].lower()

    if command in ("/dice", "/ludo"):
        value = await c.send_dice(m.chat.id, reply_to_message_id=m.id)
        await value.reply_text(f"Skorun: {value.dice.value}")
    elif command == "/dart":
        value = await c.send_dice(m.chat.id, emoji="🎯", reply_to_message_id=m.id)
        await value.reply_text(f"Skorun: {value.dice.value}")
    elif command in ("/basket", "/basketball"):
        basket = await c.send_dice(m.chat.id, emoji="🏀", reply_to_message_id=m.id)
        await basket.reply_text(f"Skorun: {basket.dice.value}")
    elif command in ("/futbol", "/football"):
        value = await c.send_dice(m.chat.id, emoji="⚽", reply_to_message_id=m.id)
        await value.reply_text(f"Skorun: {value.dice.value}")
    elif command in ("/slot", "/jackpot"):
        value = await c.send_dice(m.chat.id, emoji="🎰", reply_to_message_id=m.id)
        await value.reply_text(f"Skorun: {value.dice.value}")
    elif command == "/bowling":
        value = await c.send_dice(m.chat.id, emoji="🎳", reply_to_message_id=m.id)
        await value.reply_text(f"Skorun: {value.dice.value}")


# ────────────────────────────────────────────────
# 😐 BORED API
# ────────────────────────────────────────────────

BORED_API_URL = "https://apis.scrimba.com/bored/api/activity"


@app.on_message(filters.command("bored", prefixes=["/"]))
async def bored_command(client, message: Message):
    try:
        response = requests.get(BORED_API_URL, timeout=10)
    except Exception:
        await message.reply("Etkinlik alınamadı.")
        return

    if response.status_code == 200:
        data = response.json()
        activity = data.get("activity")
        if activity:
            await message.reply(f"Canın mı sıkıldı? Şunu dene:\n\n{activity}")
        else:
            await message.reply("Etkinlik bulunamadı.")
    else:
        await message.reply("Etkinlik alınamadı.")


# ────────────────────────────────────────────────
# 🧠 MATEMATİK OYUNU
#   - /math veya /matematik
#   - Kolay / Normal / Zor butonu
#   - Kullanıcı sadece sayı yazıyor
#   - Doğruysa otomatik yeni soru (aynı zorluk)
# ────────────────────────────────────────────────

# chat_id → {"user_id": int, "answer": int, "level": str}
math_sessions = {}


def generate_question(level: str):
    """Zorluk seviyesine göre soru üretir."""
    if level == "easy":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(["+", "-"])
    elif level == "hard":
        a = random.randint(10, 60)
        b = random.randint(10, 60)
        op = random.choice(["+", "-", "*"])
    else:  # normal
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "*"])

    # Negatif çıkmasın
    if op == "-" and b > a:
        a, b = b, a

    if op == "+":
        correct = a + b
    elif op == "-":
        correct = a - b
    else:
        correct = a * b

    return a, b, op, correct


@app.on_message(filters.command(["math", "matematik"], prefixes=["/"]))
async def start_math(client, message: Message):
    """Zorluk seçimi için buton gönderir."""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🟢 Kolay", callback_data="math_easy"),
                InlineKeyboardButton("🟡 Normal", callback_data="math_normal"),
                InlineKeyboardButton("🔴 Zor", callback_data="math_hard"),
            ]
        ]
    )

    await message.reply(
        "🧠 <b>Matematik Oyunu</b>\n\n"
        "Lütfen bir zorluk seviyesi seç:",
        reply_markup=buttons,
    )


@app.on_callback_query(filters.regex(r"^math_(easy|normal|hard)$"))
async def math_difficulty_cb(client, cq: CallbackQuery):
    """Kolay / Normal / Zor buton callback'i."""
    level = cq.data.split("_", 1)[1]  # easy / normal / hard
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id

    a, b, op, correct = generate_question(level)

    # Bu sohbetteki aktif oyuncu ve cevabı kaydet
    math_sessions[chat_id] = {
        "user_id": user_id,
        "answer": correct,
        "level": level,
    }

    level_text = {
        "easy": "Kolay",
        "normal": "Normal",
        "hard": "Zor",
    }.get(level, "Normal")

    await cq.answer(f"{level_text} seviye seçildi!", show_alert=False)

    await cq.message.edit_text(
        f"🧠 <b>Matematik Oyunu - {level_text} Seviye</b>\n\n"
        f"Soru: <code>{a} {op} {b}</code>\n\n"
        "Cevabı sadece sayı olarak yaz.\n"
        "Örneğin: <code>14</code>"
    )


@app.on_message(
    # Sadece düz metin mesajlar, komut olmayanlar
    filters.text
    & ~filters.regex(r"^/")
)
async def math_answer(client, message: Message):
    """
    Kullanıcının yazdığı sayı cevabını kontrol eder.
    - Sadece aktif oyunu olan sohbette çalışır
    - Sadece oyunu başlatan kullanıcı için çalışır
    - Doğruysa aynı zorlukta otomatik yeni soru gelir
    """
    chat_id = message.chat.id

    if chat_id not in math_sessions:
        return

    session = math_sessions[chat_id]

    # Soruyu başlatan kişi değilse görmezden gel
    if message.from_user.id != session["user_id"]:
        return

    # Mesaj sayı mı?
    try:
        user_ans = int(message.text.strip())
    except ValueError:
        # sayı değilse sessizce geç
        return

    correct = session["answer"]

    # DOĞRU CEVAP → aynı seviyeden yeni soru
    if user_ans == correct:
        level = session["level"]
        a, b, op, new_correct = generate_question(level)
        math_sessions[chat_id]["answer"] = new_correct

        await message.reply(
            "✅ <b>Doğru!</b> 🎉\n"
            "<i>Yeni soru hazır 👇</i>\n\n"
            f"📘 Soru: <code>{a} {op} {b}</code>"
        )
        return

    # YANLIŞ CEVAP → ipucu
    if user_ans > correct:
        await message.reply("❌ Yanlış. Daha küçük bir sayı dene.")
    else:
        await message.reply("❌ Yanlış. Daha büyük bir sayı dene.")


# ────────────────────────────────────────────────
# 📘 YARDIM METNİ
# ────────────────────────────────────────────────

__MODULE__ = "Eğlence"
__HELP__ = """
<b>🎲 Eğlence Komutları</b>

• <code>/dice</code> — Zar atar.
• <code>/ludo</code> — Ludo zar atar.
• <code>/dart</code> — Dart atar.
• <code>/basket</code> veya <code>/basketball</code> — Basket atışı yapar.
• <code>/football</code> veya <code>/futbol</code> — Futbol şutu dener.
• <code>/slot</code> veya <code>/jackpot</code> — Slot makinesi çevirir.
• <code>/bowling</code> — Bowling atışı yapar.
• <code>/bored</code> — Rastgele etkinlik önerir.

<b>🧠 Matematik Oyunu</b>
• <code>/math</code> veya <code>/matematik</code> — Kolay / Normal / Zor seçerek oyunu başlatır.
• Soru geldikten sonra cevabı sadece sayı olarak yazman yeterli.
• Doğru cevaptan sonra aynı zorlukta otomatik yeni soru gelir.
"""