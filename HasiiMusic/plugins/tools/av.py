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

import requests
from pyrogram import filters
from pyrogram.types import Message

from HasiiMusic import app


@app.on_message(
    filters.command(
        [
            "dice",
            "ludo",
            "dart",
            "basket",
            "basketball",
            "football",
            "slot",
            "bowling",
            "jackpot",
        ]
    )
)
async def dice(c, m: Message):
    command = m.text.split()[0]

    if command in ("/dice", "/ludo"):
        value = await c.send_dice(m.chat.id, reply_to_message_id=m.id)
        await value.reply_text("Skorun: {0}".format(value.dice.value))

    elif command == "/dart":
        value = await c.send_dice(m.chat.id, emoji="🎯", reply_to_message_id=m.id)
        await value.reply_text("Skorun: {0}".format(value.dice.value))

    elif command in ("/basket", "/basketball"):
        basket = await c.send_dice(m.chat.id, emoji="🏀", reply_to_message_id=m.id)
        await basket.reply_text("Skorun: {0}".format(basket.dice.value))

    elif command == "/football":
        value = await c.send_dice(m.chat.id, emoji="⚽", reply_to_message_id=m.id)
        await value.reply_text("Skorun: {0}".format(value.dice.value))

    elif command in ("/slot", "/jackpot"):
        value = await c.send_dice(m.chat.id, emoji="🎰", reply_to_message_id=m.id)
        await value.reply_text("Skorun: {0}".format(value.dice.value))

    elif command == "/bowling":
        value = await c.send_dice(m.chat.id, emoji="🎳", reply_to_message_id=m.id)
        await value.reply_text("Skorun: {0}".format(value.dice.value))


bored_api_url = "https://apis.scrimba.com/bored/api/activity"


@app.on_message(filters.command("bored", prefixes="/"))
async def bored_command(client, message: Message):
    # Not: requests senkron çalışır; basitlik için korunmuştur.
    # İsterseniz aiohttp/httpx ile async yapıya çevrilebilir.
    try:
        response = requests.get(bored_api_url, timeout=10)
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


__MODULE__ = "Eğlence"
__HELP__ = """
<b>🎲 Eğlence Komutları</b>

• <code>/dice</code> — Zar atar.
• <code>/ludo</code> — Ludo oynar (zar atımı).
• <code>/dart</code> — Dart atar.
• <code>/basket</code> veya <code>/basketball</code> — Basket atışı yapar.
• <code>/football</code> — Futbol şutu dener.
• <code>/slot</code> veya <code>/jackpot</code> — Slot makinesi çevirir.
• <code>/bowling</code> — Bowling atışı yapar.
• <code>/bored</code> — Canı sıkılanlar için rastgele bir etkinlik önerir.
"""


# ©️ Copyright Reserved - @NoxxOP  Nand Yaduwanshi
# ===========================================
# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# 🔗 GitHub : https://github.com/NoxxOP/ShrutiMusic
# 📢 Telegram Kanalı : https://t.me/ShrutiBots
# ===========================================
# ❤️ ShrutiBots'tan sevgiler