# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# All rights reserved.
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
            "slot",
            "bowling",
            "jackpot",
        ]
    )
)
async def dice(c, m: Message):
    cmd = m.text.split()[0].lower()

    mapping = {
        "/dice": None,
        "/ludo": None,
        "/dart": "🎯",
        "/basket": "🏀",
        "/basketball": "🏀",
        "/futbol": "⚽",
        "/football": "⚽",
        "/slot": "🎰",
        "/jackpot": "🎰",
        "/bowling": "🎳",
    }

    emoji = mapping.get(cmd)

    if emoji is None:
        value = await c.send_dice(m.chat.id, reply_to_message_id=m.id)
    else:
        value = await c.send_dice(m.chat.id, emoji=emoji, reply_to_message_id=m.id)

    await value.reply_text(f"Skorun: {value.dice.value}")


# ────────────────────────────────────────────────
# 😐 BORED
# ────────────────────────────────────────────────

@app.on_message(filters.command("bored"))
async def bored_command(_, m: Message):
    try:
        r = requests.get("https://apis.scrimba.com/bored/api/activity", timeout=10)
        data = r.json()
        act = data.get("activity")
        if act:
            return await m.reply(f"Canın mı sıkıldı? Şunu dene:\n\n{act}")
    except:
        pass

    await m.reply("Etkinlik alınamadı.")


# ────────────────────────────────────────────────
# 🧠 MATEMATİK OYUNU (BUTONLU + OTOMATİK YENİ SORU)
# ────────────────────────────────────────────────

# chat_id → {"user_id": int, "answer": int, "level": str}
math_sessions = {}


def generate_question(level):
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

    if op == "-" and b > a:
        a, b = b, a

    correct = a + b if op == "+" else (a - b if op == "-" else a * b)

    return a, b, op, correct


@app.on_message(filters.command(["math", "matematik"]))
async def start_math(_, m: Message):
    btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🟢 Kolay", callback_data="math_easy"),
                InlineKeyboardButton("🟡 Normal", callback_data="math_normal"),
                InlineKeyboardButton("🔴 Zor", callback_data="math_hard"),
            ]
        ]
    )
    await m.reply("🧠 <b>Matematik Oyunu</b>\n\nZorluk seç:", reply_markup=btn)


@app.on_callback_query(filters.regex(r"^math_(easy|normal|hard)$"))
async def math_level(_, cq: CallbackQuery):
    level = cq.data.split("_")[1]
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id

    a, b, op, correct = generate_question(level)

    math_sessions[chat_id] = {
        "user_id": user_id,
        "answer": correct,
        "level": level,
    }

    level_name = {"easy": "Kolay", "normal": "Normal", "hard": "Zor"}[level]

    await cq.message.edit_text(
        f"🧠 <b>Matematik Oyunu - {level_name}</b>\n\n"
        f"Soru: <code>{a} {op} {b}</code>\n\n"
        "Cevabı direkt sayı olarak yaz."
    )
    await cq.answer()


@app.on_message(filters.text & ~filters.command(""))
async def math_check(_, m: Message):
    chat_id = m.chat.id
    if chat_id not in math_sessions:
        return

    session = math_sessions[chat_id]

    if m.from_user.id != session["user_id"]:
        return

    # Sadece sayı cevapları dikkate al
    try:
        user_ans = int(m.text.strip())
    except:
        return

    correct = session["answer"]

    # → DOĞRU CEVAP — OTOMATİK YENİ SORU
    if user_ans == correct:
        level = session["level"]
        a, b, op, new_correct = generate_question(level)

        math_sessions[chat_id]["answer"] = new_correct

        return await m.reply(
            "✅ <b>Doğru!</b> 🎉\n"
            "<i>Yeni soru hazır 👇</i>\n\n"
            f"📘 <b>Soru:</b> <code>{a} {op} {b}</code>"
        )

    # → YANLIŞ — İPUCU
    if user_ans > correct:
        await m.reply("❌ Yanlış. Daha küçük bir sayı dene.")
    else:
        await m.reply("❌ Yanlış. Daha büyük bir sayı dene.")


# ────────────────────────────────────────────────
# 📘 YARDIM METNİ
# ────────────────────────────────────────────────

__MODULE__ = "Eğlence"
__HELP__ = """
<b>🎲 Eğlence Komutları</b>

• <code>/dice</code>
• <code>/dart</code>
• <code>/basket</code>
• <code>/football</code>
• <code>/slot</code>
• <code>/bowling</code>

<b>🧠 Matematik Oyunu</b>
• <code>/math</code> / <code>/matematik</code> — Kolay / Normal / Zor seçilir.
• Cevap direkt sayı yazılarak verilir.
• Doğru cevaptan sonra otomatik yeni soru gelir!
"""